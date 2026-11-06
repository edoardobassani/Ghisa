# v204: lista della spesa per reparto, conteggio, voci a mano, nascondi presi, condividi
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});await ctx.add_init_script("navigator.share=t=>{window.__sh=t;return Promise.resolve()}")
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
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
    await pg.click('[data-a=spsh]');await pg.wait_for_timeout(150);await pg.click('#cfm [data-a=spsht]');await pg.wait_for_timeout(150)  # foglio: link, immagine o testo
    sh=await pg.evaluate("()=>window.__sh");print('condiviso (inizio):',sh['text'][:260].replace('\n',' / '));print('  detersivo (già preso) escluso:', 'detersivo' not in sh['text'],' caffè incluso:', 'caffè' in sh['text'])
    await pg.check('#psh0');await pg.wait_for_timeout(150)
    print('nascondi presi:',await pg.evaluate("()=>document.querySelectorAll('.spi.on').length"))
    await pg.click('[data-a=ppzr]');await pg.wait_for_timeout(150);print('azzera:',await pg.evaluate("()=>document.querySelector('.spbar').textContent"))
    await pg.evaluate("()=>document.querySelector('[data-a=spxd]').click()");await pg.wait_for_timeout(150);print('voci a mano:',await pg.evaluate("()=>S.spx.map(v=>v.t)"))
    print('errori',E);await b.close()
asyncio.run(m())
