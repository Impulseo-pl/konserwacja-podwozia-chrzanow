from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg=b.new_page(viewport={'width':1440,'height':900})
    pg.goto('http://127.0.0.1:8124/konserwacja-podwozia-chrzanow/?team=1',wait_until='networkidle'); pg.wait_for_timeout(2500)
    y0=pg.evaluate("document.querySelector('.droga').getBoundingClientRect().top+scrollY")
    shots=[]
    for k,off in enumerate([-800,-450,-150]):
        pg.evaluate(f'window.scrollTo(0,{y0+off})'); pg.wait_for_timeout(700); pg.screenshot(path=f'dr{k}.png'); shots.append(f'dr{k}.png')
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300); pg.screenshot(path='dr_hero.png'); shots.append('dr_hero.png')
    ims=[Image.open(f).resize((720,450)) for f in shots]
    s=Image.new('RGB',(1440,900))
    for i,im in enumerate(ims): s.paste(im,((i%2)*720,(i//2)*450))
    s.save('dr_all.png'); b.close()
