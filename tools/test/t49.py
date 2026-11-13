# v210, aggiornato alla v230: programmi pronti separati, palestra in Schede › Palestra e cardio in Schede › Cardio
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O
st="()=>[V.tab,V.pg&&V.pg.k,(document.querySelector('.pgseg .on')||{}).textContent,(document.querySelector('#v h2')||{}).textContent,document.querySelectorAll('[data-a=cpo]').length,document.querySelectorAll('[data-a=pgo]').length]"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='s';render()}");print('tasto:',await pg.evaluate("()=>document.querySelector('[data-a=pgl]').textContent"))
    await pg.click('[data-a=pgl]');print('apertura:',await pg.evaluate(st))
    await pg.click('[data-a=pgx]');await pg.click('[data-a=skk][data-v=c]');await pg.click('[data-a=cpl]');print('cardio:',await pg.evaluate(st))
    await pg.click('[data-a=cpf][data-k]:nth-child(2)');print('filtro:',await pg.evaluate("()=>[V.pg.cf,document.querySelectorAll('[data-a=cpo]').length,V.cp]"))
    await pg.screenshot(path=O+'pg-cardio.png',full_page=True)
    await pg.click('[data-a=cpo]');print('dettaglio:',await pg.evaluate("()=>[V.tab,V.cp.id,V.cp.from,!!document.querySelector('[data-a=cpb]')]"))
    await pg.click('[data-a=cpb]');print('indietro:',await pg.evaluate(st),await pg.evaluate("()=>V.pg.cf"))
    await pg.evaluate("()=>{V.pg=null;V.tab='c';render()}");await pg.evaluate("()=>document.querySelector('[data-a=cpl]').click()");await pg.wait_for_timeout(100);print('da Cardio:',await pg.evaluate(st))
    await pg.evaluate("()=>{V.pg=null;V.tab='s';V.sk='p';render();const n=document.querySelector('[data-a=snew]');if(n)n.click();document.querySelector('[data-a=pgl]').click()}");await pg.wait_for_timeout(100);print('programmi pronti dal foglio «Nuova…» (v264):',await pg.evaluate(st),await pg.evaluate("()=>!!V.pg&&(!$('#cfm')||$('#cfm').hidden)"))
    print('errori',E);await b.close()
asyncio.run(m())
