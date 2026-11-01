# v229: riordino del menu per gruppi
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
NAV="()=>[...document.querySelectorAll('nav>.nvg,nav>button[data-t]')].map(x=>x.dataset.g?'#'+x.dataset.g:x.dataset.t).join(' ')"
async def drag(pg,sel,dy):
  h=await pg.query_selector(sel);bb=await h.bounding_box();x=bb['x']+bb['width']/2;y=bb['y']+bb['height']/2
  await pg.mouse.move(x,y);await pg.mouse.down()
  for i in range(1,16):await pg.mouse.move(x,y+dy*i/15);await pg.wait_for_timeout(30)
  await pg.wait_for_timeout(150);await pg.mouse.up();await pg.wait_for_timeout(200)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':1400})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;render();document.body.classList.add('mo')}")
    print('prima:',await pg.evaluate(NAV))
    await pg.click('[data-a=nvq]');await pg.click('[data-a=nvy]');await pg.wait_for_timeout(100)
    print('in riordino:',await pg.evaluate(NAV),'| maniglie gruppi',await pg.evaluate("()=>document.querySelectorAll('nav>.nvg>.dh').length"))
    await pg.screenshot(path=O+'v229-menu.png')
    await drag(pg,'nav>.nvg[data-g="Dati"]>.dh',-420)
    print('gruppo Dati su:',await pg.evaluate(NAV))
    await drag(pg,'nav>button[data-t="c"]>.dh',-120)
    await pg.wait_for_timeout(500);print('nord dopo 2:',await pg.evaluate("()=>S.nord&&S.nord.slice(0,6)"))
    print("Cardio su:",await pg.evaluate(NAV),await pg.evaluate("()=>[...document.querySelectorAll('.nvg')].map(x=>x.parentElement.tagName+x.className+x.style.cssText)"))
    await pg.click('[data-a=nvx]');await pg.wait_for_timeout(100)
    print('dopo Fine:',await pg.evaluate(NAV),await pg.evaluate("()=>[S.ngo,S.nord.slice(0,6)]"))
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
