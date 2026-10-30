import asyncio
from u import run
async def setup(u):
  await u.ev("()=>{xbAdd(['Panca piana bilanciere','Squat']);S.wc=1;save();render()}")
  await u.ev("()=>{V.tab='s';render()}");await u.tap('Push',exact=True);await u.fill('#scn','P');await u.tap('Crea scheda')
async def dbl(u):
  await setup(u);await u.ev("()=>{V.tab='w';V.sc=null;V.scP=0;render()}");await u.pg.select_option('#scs',label='P');await u.pg.wait_for_timeout(200);await u.tap('Inizia seduta')
  n0=await u.ev("()=>S.log.length")
  await u.fill('#ssk','40');await u.fill('#ssr','8');await u.ev("()=>{const b=document.querySelector('[data-a=ssa]');b.click();b.click()}");await u.pg.wait_for_timeout(200)
  return (n0,await u.ev("()=>S.log.length"))
async def end(u):
  await u.tap('Concludi');await u.pg.wait_for_timeout(300)
  await u.tap('Conferma: concludi');await u.pg.wait_for_timeout(300)
  await u.shot('fine');return await u.ev("()=>[V.tab,[...document.querySelectorAll('#tm,#tmr,.tmw,#tmb')].map(e=>e.id+':'+getComputedStyle(e).display+':'+e.hidden)]")
async def dl(u):
  await u.ev("()=>{V.tab='s';V.o.dSch=1;render()}")
  n=await u.ev("()=>S.sch.length");L=await u.ev("()=>[...document.querySelectorAll('#dSch button')].map(b=>b.dataset.a+':'+b.textContent.trim()).join(' | ')");print(L)
  await u.ev("()=>document.querySelector('#dSch [data-a=del]').click()");a=await u.ev("()=>S.sch.length");t=await u.text()
  await u.ev("()=>document.querySelector('#dSch [data-a=del]').click()");return (n,a,'Elimina?' in t,await u.ev("()=>S.sch.length"))
asyncio.run(run([('doppio tocco',dbl),('fine seduta',end),('elimina',dl)]))
