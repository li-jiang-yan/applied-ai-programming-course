"""Focused integrity checks for the generated teaching artifact."""
import ast
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.videos = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate id: {attrs['id']}"
            self.ids.add(attrs['id'])
        for key in ['href', 'src']:
            if key in attrs: self.links.append(attrs[key])
        if tag == 'img':
            assert attrs.get('alt'), 'Missing alt text'
            self.images.append(attrs)
        if tag == 'iframe':
            assert attrs.get('title'), 'Missing iframe title'
            self.videos.append(attrs)

def main():
    pages = [ROOT/'index.html'] + [ROOT/f'module-{i:02}.html' for i in range(2,7)]
    parsed = {}
    for i, path in enumerate(pages, 1):
        parser = Page()
        text = path.read_text(encoding='utf-8')
        parser.feed(text)
        assert '{{code:' not in text
        assert {'overview','lecture','watch','lab','solutions','check','summary'} <= parser.ids
        steps = text.count('class="lab-step"')
        assert steps > 0
        for step in range(1, steps + 1):
            assert f'solution-{step}' in parser.ids, f'Missing worked solution: module {i}, step {step}'
            assert f'href="#solution-{step}"' in text
        assert text.index('id="lab"') < text.index('id="solutions"') < text.index('id="check"')
        assert len(parser.images) >= 2 and parser.videos
        curriculum = (ROOT/'curriculum'/f'module_{i:02}.md').read_text(encoding='utf-8')
        objectives = re.findall(r'^- (.+)', curriculum.split('## Learning Objectives')[1], re.M)
        import html
        for objective in objectives:
            assert html.escape(objective) in text, f'Missing objective: {objective}'
        parsed[path] = parser
    for path, parser in parsed.items():
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc: continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target.exists(), f'Broken link: {path.name}: {link}'
            if url.fragment and target in parsed:
                assert url.fragment in parsed[target].ids, f'Broken anchor: {link}'
    for path in (ROOT/'assets').glob('*.svg'): ET.parse(path)
    for path in (ROOT/'labs').rglob('*.py'): ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    with zipfile.ZipFile(ROOT/'labs.zip') as z:
        assert z.testzip() is None
        assert 'labs/data/refund.txt' in z.namelist()
        for path in (ROOT/'labs').rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                assert z.read(path.relative_to(ROOT).as_posix()) == path.read_bytes()
    def run(*args):
        return subprocess.check_output([sys.executable,*args],cwd=ROOT/'labs',text=True,encoding='utf-8')
    assert 'refund.txt' in run('module04/retrieval.py')
    assert '7 days' in run('module06/agent.py','When can I request a refund?')
    assert 'do not have a policy' in run('module06/agent.py','Is parking included?')
    assert 'budget exhausted' in run('module06/agent.py','refund','--max-steps','1')
    assert 'estimated_rewards' in run('module06/bandit.py')
    print('PASS: six pages; objectives, local links/anchors, images, embeds, source syntax, archive, and offline labs.')

if __name__ == '__main__': main()
