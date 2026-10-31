# v205: vista Settimana del piano pasti (tabella giorni × pasti, colori rispetto all'obiettivo, tocco apre il giorno)
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8780','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8780/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='pp';V.pv='w';render()}");print('vuoto:',await pg.evaluate("()=>document.querySelector('#v .hint:last-of-type').textContent.slice(0,40)"))
    await pg.evaluate("()=>{S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.dp={id:'sce'};render()}")
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{const d=ppD(2);d.Cena=d.Cena.slice(0,1);V.pv='w';render()}")
    print('righe:',await pg.evaluate("()=>[...document.querySelectorAll('.pwr')].map(r=>r.innerText.replace(/\\s+/g,' ')).join(' | ')"))
    print('colori:',await pg.evaluate("()=>[...document.querySelectorAll('.pwk')].map(e=>e.className.split(' ')[1]||'-').join(',')"))
    await pg.screenshot(path=O+'pw.png',full_page=True)
    await pg.click('.pwr[data-i="2"]');await pg.wait_for_timeout(200)
    print('aperto:',await pg.evaluate("()=>[V.pv,V.pj,document.querySelector('#v .card h2').textContent.slice(0,20)]"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
