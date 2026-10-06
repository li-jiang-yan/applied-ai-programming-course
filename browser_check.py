"""Local browser smoke check; external video requests are excluded."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={"width":1440,"height":1000})
    context.route('https://www.youtube-nocookie.com/**', lambda route: route.abort())
    page = context.new_page()
    errors=[]
    page.on('pageerror', lambda error: errors.append(str(error)))
    for filename in ['index.html']+[f'module-{i:02}.html' for i in range(2,7)]:
        response=page.goto(f'http://127.0.0.1:8000/{filename}',wait_until='domcontentloaded')
        assert response.status == 200
        assert page.locator('h1').count()==1
        assert page.locator('#solutions').count()==1
        assert page.locator('#solutions details[open]').count()==0
        page.locator('.lab-step a[href="#solution-1"]').click()
        assert page.locator('#solution-1').evaluate('(node) => node.open')
        page.locator('#solution-1 > summary').click()
        assert not page.locator('#solution-1').evaluate('(node) => node.open')
        page.locator('.lab-step a[href="#solution-1"]').click()
        assert page.locator('#solution-1').evaluate('(node) => node.open')
        assert page.locator('img').evaluate_all('(xs) => xs.every(x => x.complete && x.naturalWidth > 0)')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.goto('http://127.0.0.1:8000/index.html',wait_until='domcontentloaded')
    page.locator('#complete').check()
    page.reload(wait_until='domcontentloaded')
    assert page.locator('#complete').is_checked()
    assert page.locator('progress').get_attribute('value')=='1'
    page.locator('.course-nav a[href="projects.html"]').click()
    assert page.locator('.course-nav a[aria-current="page"]').get_attribute('href')=='projects.html'
    assert page.locator('progress').get_attribute('value')=='1'
    assert page.locator('progress').get_attribute('max')=='6'
    assert page.locator('#complete').count()==0
    assert page.locator('section.project').count()==6
    for project in page.locator('section.project').all():
        assert project.locator('a[href*=".html#"]').count() >= 2
        project.locator('summary').click()
        assert project.locator('details').evaluate('(node) => node.open')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0)")
    page.screenshot(path=str(ROOT/'preview-projects.png'))
    page.goto('http://127.0.0.1:8000/index.html',wait_until='domcontentloaded')
    page.locator('#complete').uncheck()
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0)")
    page.screenshot(path=str(ROOT/'preview-desktop.png'))
    page.goto('http://127.0.0.1:8000/module-04.html',wait_until='domcontentloaded')
    page.locator('#top-k').fill('5')
    assert page.locator('#retrieved li').count()==5
    page.set_viewport_size({"width":390,"height":844})
    page.goto('http://127.0.0.1:8000/projects.html',wait_until='domcontentloaded')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.locator('#project-1 summary').click()
    assert page.locator('#project-1 details').evaluate('(node) => node.open')
    for filename in ['index.html']+[f'module-{i:02}.html' for i in range(2,7)]:
        page.goto(f'http://127.0.0.1:8000/{filename}',wait_until='domcontentloaded')
        page.locator('.lab-step a[href="#solution-1"]').click()
        assert page.locator('#solution-1').evaluate('(node) => node.open')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), filename
    page.goto('http://127.0.0.1:8000/index.html',wait_until='domcontentloaded')
    page.screenshot(path=str(ROOT/'preview-mobile.png'))
    assert not errors, errors
    browser.close()
print('PASS: desktop/mobile core and project pages, project hints and navigation, six-module progress, solution links, images, RAG slider, no JavaScript errors.')
