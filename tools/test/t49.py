# v210: programmi pronti di palestra e cardio insieme in Schede, con i tasti Palestra/Cardio
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8785','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
st="()=>[V.tab,V.pg&&V.pg.k,(document.querySelector('.pgseg .on')||{}).textContent,(document.querySelector('#v h2')||{}).textContent,document.querySelectorAll('[data-a=cpo]').length,document.querySelectorAll('[data-a=pgo]').length]"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8785/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='s';render()}");print('tasto:',await pg.evaluate("()=>document.querySelector('[data-a=pgl]').textContent"))
    await pg.click('[data-a=pgl]');print('apertura:',await pg.evaluate(st))
    await pg.click('[data-a=pgk][data-v=c]');print('cardio:',await pg.evaluate(st))
    await pg.click('[data-a=cpf][data-k]:nth-child(2)');print('filtro:',await pg.evaluate("()=>[V.pg.cf,document.querySelectorAll('[data-a=cpo]').length,V.cp]"))
    await pg.screenshot(path=O+'pg-cardio.png',full_page=True)
    await pg.click('[data-a=cpo]');print('dettaglio:',await pg.evaluate("()=>[V.tab,V.cp.id,V.cp.from,!!document.querySelector('[data-a=cpb]')]"))
    await pg.click('[data-a=cpb]');print('indietro:',await pg.evaluate(st),await pg.evaluate("()=>V.pg.cf"))
    await pg.reload();await pg.wait_for_timeout(900);await pg.evaluate("()=>{V.tab='s';V.pg=null;V.cp=null;render()}");await pg.click('[data-a=pgl]');print('ricorda la scelta:',await pg.evaluate(st))
    await pg.evaluate("()=>{V.pg=null;V.tab='c';render()}");await pg.evaluate("()=>document.querySelector('[data-a=cpl]').click()");await pg.wait_for_timeout(100);print('da Cardio:',await pg.evaluate(st))
    await pg.evaluate("()=>{V.pg=null;V.tab='s';render();document.querySelector('[data-a=bppr]').click()}");await pg.wait_for_timeout(100);print('scorciatoia blocchi:',await pg.evaluate(st),await pg.evaluate("()=>V.pg.f"))
    await pg.click('[data-a=pgk][data-v=p]')
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
