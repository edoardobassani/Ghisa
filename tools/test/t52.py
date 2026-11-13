# v213: striscia della settimana in Dieta e scorrimento tra i giorni (Dieta e Piano pasti · Giorno)
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
SWIPE="""async([sel,dx])=>{const el=document.querySelector(sel),r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+Math.min(40,r.height/2);
 const T=(cx)=>new Touch({identifier:1,target:el,clientX:cx,clientY:y});
 el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[T(x)],changedTouches:[T(x)]}));
 for(let i=1;i<=5;i++)el.dispatchEvent(new TouchEvent('touchmove',{bubbles:true,touches:[T(x+dx*i/5)],changedTouches:[T(x+dx*i/5)]}));
 el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[T(x+dx)]}));await new Promise(r=>setTimeout(r,60))}"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True);pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.goal=2000;const f=allF()[0];[[-1,1200],[0,1000]].forEach(([o,g],i)=>S.meal.push({id:'tm'+i,d:hvAdd(today(),o),m:'Pranzo',f:f.id,g:g*100/f.k}));V.tab='n';V.nd=today();render()}")
    n=await pg.evaluate("()=>[document.querySelectorAll('.dwk button').length,document.querySelector('.dwk button.on').dataset.v==today(),!!document.querySelector('.dswh')]")
    print('striscia: 7 giorni, oggi selezionato, avviso visibile:',n)
    await pg.screenshot(path=O+'v213-strip.png')
    await pg.click('.dwk button:nth-child(1)');print('tocco su lunedì:',await pg.evaluate("()=>V.nd==hvMon(today())"))
    await pg.evaluate("()=>{V.nd=today();render()}")
    await pg.evaluate(SWIPE,['[data-blk=tot]',150]);print('scorri a destra -> ieri:',await pg.evaluate("()=>V.nd==hvAdd(today(),-1)"),'avviso sparito:',await pg.evaluate("()=>!document.querySelector('.dswh')&&localStorage.getItem('gymbo-swd')=='1'"))
    await pg.evaluate(SWIPE,['[data-blk=tot]',-150]);print('scorri a sinistra -> oggi:',await pg.evaluate("()=>V.nd==today()"))
    await pg.evaluate(SWIPE,['[data-blk=tot]',-40]);print('gesto corto non cambia:',await pg.evaluate("()=>V.nd==today()"))
    await pg.evaluate(SWIPE,['#nd',-150]);print('su un campo non cambia:',await pg.evaluate("()=>V.nd==today()"))
    # piano pasti, vista Giorno
    await pg.evaluate("()=>{V.tab='pp';V.ppz=1;V.pv='p';V.pj=6;render()}")
    w0=await pg.evaluate("()=>V.pw||hvMon(today())")
    await pg.evaluate(SWIPE,['.ppds',-150]);print('piano: domenica -> lunedì della settimana dopo:',await pg.evaluate("w=>[V.pj==0,V.pw==hvAdd(w,7)]",w0))
    await pg.evaluate(SWIPE,['#v h1',150]);print('piano: indietro -> domenica prima:',await pg.evaluate("w=>[V.pj==6,(V.pw||hvMon(today()))==w]",w0))
    await pg.evaluate("()=>{V.pv='w';render()}");j=await pg.evaluate("()=>V.pj")
    await pg.evaluate(SWIPE,['#v h1',-150]);print('vista Settimana: niente scorrimento:',await pg.evaluate("j=>V.pj==j",j))
    await pg.evaluate("()=>{V.tab='h';render()}");await pg.evaluate(SWIPE,['#v h1',-150]);print('Home: niente scorrimento:',await pg.evaluate("()=>V.tab=='h'"))
    await pg.emulate_media(color_scheme='dark');await pg.evaluate("()=>{V.tab='n';V.nd=today();render()}");await pg.screenshot(path=O+'v213-dark.png')
    print('errori',E);await b.close()
asyncio.run(m())
