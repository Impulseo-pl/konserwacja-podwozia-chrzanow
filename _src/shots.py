import sys
from playwright.sync_api import sync_playwright
from PIL import Image
pages=sys.argv[2].split(',') ; w=int(sys.argv[1]); mobile=w<700
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':900 if not mobile else 844},device_scale_factor=1,is_mobile=mobile,has_touch=mobile)
    pg=ctx.new_page()
    errs=[]; pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
    for path in pages:
        pg.goto('http://127.0.0.1:8124/konserwacja-podwozia-chrzanow/'+path+('?team=1'),wait_until='networkidle')
        h=pg.evaluate('document.body.scrollHeight')
        for y in range(0,h,600): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(120)
        pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(1500)
        sw=pg.evaluate('document.documentElement.scrollWidth')
        name=(path.strip('/') or 'home').replace('/','_')+f'_{w}'
        pg.screenshot(path=f'sh_{name}.png',full_page=True)
        i=Image.open(f'sh_{name}.png'); tw=720 if not mobile else 390
        i=i.resize((tw,int(i.height*tw/i.width))); n=0; step=1900 if not mobile else 1700
        for y in range(0,i.height,step): i.crop((0,y,tw,min(y+step,i.height))).save(f'sh_{name}_{n}.png'); n+=1
        print(name,'h',h,'scrollW',sw,'parts',n)
    print('errors',errs)
    b.close()
