# v204: lista della spesa per reparto, conteggio, voci a mano, nascondi presi, condividi
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8779','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});await ctx.add_init_script("navigator.share=t=>{window.__sh=t;return Promise.resolve()}")
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8779/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.tab='pp';V.dp={id:'sce'};render()}")
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(200)
    await pg.click('[data-a=ppv][data-v=s]');await pg.wait_for_timeout(200)
    print('reparti:',await pg.evaluate("()=>[...document.querySelectorAll('.spc h2')].map(e=>e.textContent).join(' | ')"))
    print('barra:',await pg.evaluate("()=>document.querySelector('.spbar').textContent"))
    await pg.evaluate("()=>document.querySelectorAll('.ppc')[0].click()");await pg.wait_for_timeout(150)
    await pg.fill('#spxi','detersivo, caffè');await pg.click('[data-a=spxa]');await pg.wait_for_timeout(150)
    await pg.evaluate("()=>document.querySelector('.spxc').click()");await pg.wait_for_timeout(150)
    print('dopo spunte:',await pg.evaluate("()=>document.querySelector('.spbar').textContent"))
    await pg.screenshot(path=O+'sp-lista.png',full_page=True)
    await pg.click('[data-a=spsh]');await pg.wait_for_timeout(150)
    sh=await pg.evaluate("()=>window.__sh");print('condiviso (inizio):',sh['text'][:260].replace('\n',' / '));print('  contiene detersivo:', 'detersivo' in sh['text'],' caffè:', 'caffè' in sh['text'])
    await pg.check('#psh0');await pg.wait_for_timeout(150)
    print('nascondi presi:',await pg.evaluate("()=>document.querySelectorAll('.spi.on').length"))
    await pg.click('[data-a=ppzr]');await pg.wait_for_timeout(150);print('azzera:',await pg.evaluate("()=>document.querySelector('.spbar').textContent"))
    await pg.evaluate("()=>document.querySelector('[data-a=spxd]').click()");await pg.wait_for_timeout(150);print('voci a mano:',await pg.evaluate("()=>S.spx.map(v=>v.t)"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
