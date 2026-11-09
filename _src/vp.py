import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg=b.new_page(viewport={'width':1440,'height':900})
    pg.goto('http://127.0.0.1:8124/konserwacja-podwozia-chrzanow/?team=1',wait_until='networkidle'); pg.wait_for_timeout(2500)
    for i in [1,3,6]:
        pg.evaluate(f"document.querySelector('.krok[data-s=\"{i}\"]').scrollIntoView({{block:'center'}})"); pg.wait_for_timeout(1600)
        pg.screenshot(path=f'vp_krok{i}.png')
    pg.click('#tab-starsze'); pg.evaluate("document.getElementById('auta').scrollIntoView()"); pg.wait_for_timeout(1500); pg.screenshot(path='vp_tab.png')
    b.close()
