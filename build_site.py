"""Build the six course pages using only the Python standard library."""
from pathlib import Path
import html
import re
import zipfile

ROOT = Path(__file__).resolve().parent
NAMES = ['LLMs & your first AI app', 'Interfaces with Gradio & Streamlit', 'LangChain & visual workflows', 'Retrieval augmented generation', 'Fine-tuning language models', 'Programming AI agents']
TITLES = ['From language models to working applications', 'Make your AI application usable', 'Connect models, tools, and data', 'Give your model evidence to work with', 'Teach a pretrained model a new task', 'Build agents that decide, act, and learn']
DESCRIPTIONS = ['Understand the building blocks, make your first model calls, and turn local course notes into a question-answering app.', 'Build two interfaces for the same model. Learn how inputs, state, feedback, and deployment shape the user experience.', 'Compose a Python pipeline, prototype it visually, and call your exported workflows from an application.', 'Build a grounded helpdesk, inspect its retrieval, tune its components, and measure what actually improves.', 'Prepare trustworthy datasets, adapt pretrained models, and compare results on examples they have never seen.', 'Move from fixed rules to bounded tool use, coordinated roles, and a small agent that learns from feedback.']
FILES = ['index.html'] + [f'module-{i:02}.html' for i in range(2,7)]
LEVELS = ['Foundation', 'Foundation → intermediate', 'Intermediate', 'Intermediate → advanced', 'Intermediate → advanced', 'Intermediate → advanced']
MAPS = [[1,1,2,2,3,4,5],[1,2,3,4,5],[1,1,2,3,4,5],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6]]
EXTRA_VIDEOS = {
    2: [
        ('LS9Y2wDVI0k', 'Host a Gradio demo on Hugging Face Spaces', 'Follow the deployment demonstration embedded in the official Hugging Face course. Use it alongside lab step 5; hosting menus and resource policies can change.'),
        ('4sPnOqeUDmk', 'Streamlit chat elements with Chanin Nantasenamat', 'The tutorial embedded in the official Streamlit documentation extends the interface lesson to chat messages and input. Connect it with the session-state discussion in Lesson 5.'),
    ],
    5: [('rNgUoH7Wbv8', 'Training Agents: supervised fine-tuning walkthrough · Hugging Face', 'Advanced video alternative for the training workflow: watch data formatting, TRL and LoRA configuration, and evaluation. This uses coding-agent traces rather than the small datasets in our lab. Return to the task-specific checks for sentiment and NER.')],
}

def bullets(section):
    return re.findall(r'^- (.+)', section, re.M)

def diagram(name, title, boxes, caption):
    # Original vector teaching illustrations, not simulated product screenshots.
    w=900; boxw=245
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 290" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(caption)}</desc><rect width="900" height="290" fill="#f4f8f5"/><text x="35" y="42" font-family="sans-serif" font-size="21" font-weight="700" fill="#173c42">{html.escape(title)}</text>']
    for i,(label,lines) in enumerate(boxes):
        x=35+i*290
        parts.append(f'<rect x="{x}" y="75" width="{boxw}" height="145" rx="12" fill="white" stroke="#9ebeb3"/><circle cx="{x+25}" cy="104" r="13" fill="#006d67"/><text x="{x+25}" y="110" text-anchor="middle" font-family="sans-serif" font-size="15" fill="white">{i+1}</text><text x="{x+47}" y="110" font-family="sans-serif" font-size="17" font-weight="700" fill="#173c42">{html.escape(label)}</text>')
        for j,line in enumerate(lines):
            parts.append(f'<text x="{x+17}" y="{145+j*25}" font-family="sans-serif" font-size="15" fill="#37545b">{html.escape(line)}</text>')
        if i<2: parts.append(f'<path d="M {x+252} 150 h 28 m -9 -7 l 9 7 -9 7" fill="none" stroke="#006d67" stroke-width="3"/>')
    parts.append(f'<text x="35" y="260" font-family="sans-serif" font-size="14" fill="#526570">{html.escape(caption)}</text></svg>')
    (ROOT/'assets'/f'{name}.svg').write_text(''.join(parts),encoding='utf-8')

DIAGRAMS = [
('m1-input','A model call has three distinct parts',[('Prepare',['Instruction + question','Use fictional data']),('Run',['Python SDK → provider','Model predicts tokens']),('Inspect',['Read response text','Check against evidence'])],'Lab 1 • The prompt is input; the generated answer still needs checking.'),
('m1-rag','Your first document question-answering app',[('Index',['course.txt → chunks','Chunks → embeddings']),('Retrieve',['Question → embedding','Select matching chunks']),('Answer',['Context + question → LLM','Show answer and sources'])],'Lab 1 • Hosted embedding and generation calls send text outside your computer.'),
('m2-ui','One model, two interface styles',[('Inputs',['Review text','Threshold + display mode']),('Function',['Validate → classify','Return label and score']),('Outputs',['Prediction + uncertainty','Session request counter'])],'Lab 2 • The same predict function powers Gradio and Streamlit.'),
('m2-deploy','From your laptop to a hosted demo',[('Package',['app.py + backend.py','requirements.txt']),('Configure',['Choose hosting runtime','Set secrets on server']),('Verify',['Open in another browser','Test errors and concurrency'])],'Lab 2 • A successful local run is only the first deployment checkpoint.'),
('m3-flow','Draw the same pipeline in both visual tools',[('Input',['Chat Input / question','A named input variable']),('Compose',['Prompt template','Chat model + credentials']),('Output',['Chat Output / response','Save → export flow JSON'])],'Lab 3 • Node labels vary by release; preserve the input → prompt → model contract.'),
('m3-api','A flow export and an API call are different artifacts',[('Export',['Download workflow JSON','Remove embedded secrets']),('Restore',['Import into runtime','Reconnect credentials']),('Call',['Python → runtime API','Parse response JSON'])],'Lab 3 • A JSON export is not a standalone Python application.'),
('m4-retrieve','Trace an answer back to a source',[('Question',['When can I get a refund?','Embed the query']),('Evidence',['refund.txt / chunk 1','7 days before the start']),('Answer',['State the deadline','Attach the source filename'])],'Lab 4 • Inspect retrieved chunks before judging generated prose.'),
('m4-eval','Evaluate components separately',[('Retrieval',['Gold relevant source IDs','Recall@k and rank']),('Generation',['Supported claims','Correctness and abstention']),('Operation',['Latency and token use','Compare before / after'])],'Lab 4 • Better wording cannot compensate for missing evidence.'),
('m5-data','Keep evaluation data out of training',[('Training',['Examples + labels','Update model parameters']),('Validation',['Choose hyperparameters','Select a checkpoint']),('Test',['One final comparison','Report unseen performance'])],'Lab 5 • Split related examples together before augmentation.'),
('m5-train','Read learning curves as a diagnostic',[('Healthy fit',['Train loss decreases','Validation also improves']),('Overfitting',['Train keeps improving','Validation gets worse']),('Respond',['Earlier checkpoint','More data / regularization'])],'Lab 5 • These are schematic patterns, not measured results from the lab.'),
('m6-loop','A bounded agent loop',[('Observe',['Goal + tool results','Keep explicit state']),('Decide',['Choose an allowed tool','Validate its arguments']),('Act & check',['Run → log observation','Finish or stop at budget'])],'Lab 6 • Tool execution belongs to the application, not to generated text.'),
('m6-team','Coordinate by passing evidence',[('Researcher',['Find relevant policy','Return source and quote']),('Reviewer',['Check claim support','Accept or request revision']),('Coordinator',['Own task and budget','Stop after bounded retries'])],'Lab 6 • Separate roles help only when their outputs can be checked.'),
]

def main():
    for args in DIAGRAMS: diagram(*args)
    for i in range(1,7):
        source=(ROOT/'curriculum'/f'module_{i:02}.md').read_text(encoding='utf-8')
        audience=bullets(source.split('## Who Should Attend')[1].split('## PREREQUISITES')[0])
        prereq=bullets(source.split('## PREREQUISITES')[1].split('## Overview')[0])
        objectives=bullets(source.split('## Learning Objectives')[1])
        nav=''.join(f'<a href="{f}"'+(' aria-current="page"' if j==i-1 else '')+f'><b>{j+1:02}</b><span>{html.escape(NAMES[j])}</span></a>' for j,f in enumerate(FILES))
        rows=''.join(f'<tr><td>{n}</td><td>{html.escape(o)}</td><td><a href="#lesson-{MAPS[i-1][n-1]}">Lesson {MAPS[i-1][n-1]}</a> + lab</td></tr>' for n,o in enumerate(objectives,1))
        body=(ROOT/'content'/f'module-{i:02}.html').read_text(encoding='utf-8')
        solutions=(ROOT/'content'/f'solutions-{i:02}.html').read_text(encoding='utf-8')
        step_number = 0
        def solution_link(match):
            nonlocal step_number
            step_number += 1
            return match.group(0) + f'<p class="small"><a href="#solution-{step_number}">Stuck? See the worked solution for this step →</a></p>'
        body=re.sub(r'<div class="lab-step"><h3>.*?</h3>', solution_link, body)
        body=body.replace('<section id="check">', solutions + '\n<section id="check">', 1)
        extra=''.join(f'<article class="video-card"><h3>{html.escape(title)}</h3><iframe class="video" src="https://www.youtube-nocookie.com/embed/{vid}" title="{html.escape(title)}" loading="lazy" allowfullscreen></iframe><p>{html.escape(description)} <a href="https://www.youtube.com/watch?v={vid}">Watch on YouTube</a>.</p></article>' for vid,title,description in EXTRA_VIDEOS.get(i, []))
        if extra:
            marker='<section id="lab"'
            before, after=body.split(marker,1)
            end=before.rfind('</section>')
            body=before[:end]+extra+before[end:]+marker+after
        # Include downloadable source verbatim so the course and lab cannot drift.
        def embed(match):
            path=match.group(1)
            return f'<p><a href="labs/{path}" download>Download {html.escape(path)}</a></p><pre><code>{html.escape((ROOT/"labs"/path).read_text(encoding="utf-8"))}</code></pre>'
        body=re.sub(r'\{\{code:([^}]+)\}\}',embed,body)
        prev=f'<a href="{FILES[i-2]}">← Module {i-1}</a>' if i>1 else '<a href="#overview">Back to overview</a>'
        nxt=f'<a class="button" href="{FILES[i]}">Module {i+1} →</a>' if i<6 else '<a class="button" href="index.html">Revisit the course →</a>'
        page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{DESCRIPTIONS[i-1]}"><title>Module {i} · {NAMES[i-1]} | Applied AI Studio</title><link rel="stylesheet" href="assets/style.css"><script src="assets/course.js" defer></script></head>
<body data-module="{i}"><a class="skip" href="#main">Skip to lesson</a><header class="topbar"><a class="brand" href="index.html"><b>ai</b> Applied AI Studio</a><span>PUBLIC LEARNING SERIES &nbsp; / &nbsp; 6 PRACTICAL MODULES</span><a href="labs.zip" download>Lab files ↓</a></header>
<div class="layout"><aside class="sidebar"><div class="eyebrow">Your learning path</div><nav class="course-nav" aria-label="Modules">{nav}</nav><progress value="0" max="6" aria-label="Course completion"></progress><p class="progress-text small" aria-live="polite">0 of 6 modules marked complete</p><nav class="toc" aria-label="On this page"><a href="#overview">Overview & outcomes</a><a href="#lecture">Read the lecture</a><a href="#watch">Watch & learn</a><a href="#lab">Guided lab</a><a href="#solutions">Lab solutions</a><a href="#check">Check your understanding</a><a href="#summary">Module summary</a></nav></aside>
<main id="main"><header class="hero"><div class="eyebrow">Module {i:02} / 06 · Learn by building</div><h1>{TITLES[i-1]}</h1><p>{DESCRIPTIONS[i-1]}</p><div class="chips"><span>2 days · 12 learning hours</span><span>{LEVELS[i-1]}</span><span>Python</span></div><a class="button" href="#lab">Explore the guided lab ↗</a></header>
<section id="overview"><div class="eyebrow">Start here</div><h2>{NAMES[i-1]}</h2><p>Read the lecture or follow the video route, then complete the illustrated lab and the checks. The videos cover selected concepts; the short bridge notes identify the remaining material. Allow six learning hours per day, with breaks in addition.</p><details><summary>Who this module is for & prerequisites</summary><p><strong>Audience:</strong> {html.escape('; '.join(audience))}.</p><ul>{''.join(f'<li>{html.escape(p)}</li>' for p in prereq)}</ul><p>New to Python? Before starting, practise defining a function, importing a package, reading a text file, using a dictionary, and creating a virtual environment. Later modules provide a short bridge back to these skills.</p></details><details><summary>Learning objectives — mapped to the curriculum</summary><div class="table-wrap"><table><thead><tr><th>#</th><th>Curriculum objective</th><th>Where to learn it</th></tr></thead><tbody>{rows}</tbody></table></div></details></section>
{body}
<label class="complete"><input type="checkbox" id="complete">I completed the lab and can explain the module outcomes.</label><p class="small">Progress is stored in this browser when storage is available. It is a personal checklist, not a certificate or assessment record.</p><nav class="pager" aria-label="Continue learning">{prev}{nxt}</nav><footer class="footer">Applied AI Studio · Original teaching text and illustrations · Reference review: 25 September 2026.<br>External videos belong to their creators. Playback, captions, accounts, and model availability depend on the provider.</footer></main></div></body></html>'''
        (ROOT/FILES[i-1]).write_text(page,encoding='utf-8')
    with zipfile.ZipFile(ROOT/'labs.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in (ROOT/'labs').rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                z.write(path,path.relative_to(ROOT))
    print('Built six module pages, twelve illustrations, and labs.zip.')

if __name__=='__main__': main()
