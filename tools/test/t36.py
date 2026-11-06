# v194: piano pronto «A scelta, stile nutrizionista» (sce): alimenti esistenti, 7 giorni, applicazione al piano
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    print('piani',await pg.evaluate("()=>DPM.length"),'mancanti',await pg.evaluate("()=>{const p=DPM.find(x=>x[0]=='sce');return p.slice(5).flat().flatMap(dpIt).filter(x=>!dpFood(x.n)).map(x=>x.n)}"))
    await pg.evaluate("()=>{S.wc=1;S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.tab='pp';V.dp={id:'sce'};render()}")
    await pg.evaluate("()=>document.querySelector('[data-a=dpu]').click()");await pg.wait_for_timeout(200)
    await pg.evaluate("()=>document.querySelector('[data-a=dpok]').click()");await pg.wait_for_timeout(300)
    print(await pg.evaluate("()=>[document.querySelector('#toast').textContent,S.goal,[0,1,2,3,4,5,6].map(d=>Math.round(ppTot(d).k))]"))
    print('errori',E);await b.close()
asyncio.run(m())
