# v214: dimensione del testo a 5 misure (zoom della pagina) e coordinate corrette con lo zoom
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;xbAdd(['Panca piana bilanciere']);const id=S.ex[0].id;S.sch.push({id:'sx',name:'Prova',ex:[id],t:{[id]:{s:3,r:8}},rt:{[id]:90}});V.tab='h';render()}")
    await pg.click('#mb');await pg.wait_for_timeout(250)
    print('voce nel menu:',await pg.evaluate("()=>$('.tszb').innerText.replace(/\\n/g,' ')"))
    await pg.click('[data-a=tszo]');await pg.wait_for_timeout(200)
    print('foglio aperto, menu chiuso:',await pg.evaluate("()=>[!$('#cfm').hidden,$('#cfm').classList.contains('tsz'),!document.body.classList.contains('mo'),document.querySelectorAll('[data-a=tsz]').length]"))
    await pg.screenshot(path=O+'v214-sheet.png')
    for v,z in [(2,1.3),(1,1.15),(-1,0.85),(-2,0.7),(0,1)]:
      await pg.click(f'[data-a=tsz][data-v="{v}"]');await pg.wait_for_timeout(120)
      r=await pg.evaluate("()=>[getComputedStyle(document.documentElement).zoom,S.ts,$('[data-a=tsz][aria-pressed=true]').dataset.v,!$('#cfm').hidden]")
      print('misura',v,'->',r,'atteso zoom',z)
    await pg.click('[data-a=tsz][data-v="2"]');await pg.click('[data-a=tszx]');print('Fatto chiude:',await pg.evaluate("()=>$('#cfm').hidden"))
    # menu laterale e larghezza della pagina con Molto grande
    await pg.click('#mb');await pg.wait_for_timeout(300)
    nr=await pg.evaluate("()=>{const r=$('nav').getBoundingClientRect();return [Math.round(r.right),innerWidth,![...document.querySelectorAll('#v *')].some(e=>e.getBoundingClientRect().right>innerWidth+1)]}")
    print('menu dentro lo schermo, niente scorrimento laterale:',nr[0]<=nr[1],nr[2]);await pg.screenshot(path=O+'v214-menu-xl.png')
    await pg.evaluate('()=>openM(false)');await pg.wait_for_timeout(250)
    # dopo il riavvio la misura resta
    await pg.evaluate("()=>{dFlush&&dFlush()}");await pg.wait_for_timeout(400);await pg.reload();await pg.wait_for_timeout(900)
    print('dopo il riavvio:',await pg.evaluate("()=>[S.ts,getComputedStyle(document.documentElement).zoom]"))
    await pg.evaluate("()=>{S.wc=1;V.tab='h';render()}");await pg.screenshot(path=O+'v214-home-xl.png')
    # seduta con timer: il cerchio resta nello schermo e si sposta dove si trascina
    await pg.evaluate("()=>{V.ss={sid:'ss1',sc:'sx',fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};V.tab='ss';render();tStart(90)}");await pg.wait_for_timeout(300)
    t=await pg.evaluate("()=>{const r=$('#tm').getBoundingClientRect();return [r.left>=0,r.right<=innerWidth,r.bottom<=innerHeight]}");print('timer dentro lo schermo:',t)
    bx=await pg.evaluate("()=>{const r=$('#tm').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")
    await pg.mouse.move(*bx);await pg.mouse.down();await pg.mouse.move(200,300,steps=8);await pg.mouse.move(200,400,steps=8);await pg.mouse.up();await pg.wait_for_timeout(150)
    c=await pg.evaluate("()=>{const r=$('#tm').getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]}");print('timer trascinato a (200,400):',c)
    await pg.screenshot(path=O+'v214-seduta-xl.png')
    await pg.mouse.click(c[0],c[1]);await pg.wait_for_timeout(150)
    mm=await pg.evaluate("()=>{const m=$('#tmm').getBoundingClientRect();return [m.left>=0,m.right<=innerWidth+1,m.top>=0,$('#tmm').classList.contains('on')]}");print('menu del timer nello schermo:',mm)
    await pg.evaluate("()=>{tmHide();S.ts=-2;applyTs();V.ss=null;V.tab='n';render()}");await pg.screenshot(path=O+'v214-dieta-xs.png')
    print('errori',E);await b.close()
asyncio.run(m())
