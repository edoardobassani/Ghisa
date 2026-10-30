import asyncio
from u import run
async def a(u):
  await u.shot('home-new');t=await u.text();assert 'Benvenuto' in t,'no card';return t.split('Nascondi')[0][-200:].replace('\n',' | ')
async def b(u):
  await u.tap('Scegli un programma');return await u.ev("()=>V.tab")
async def c(u):
  await u.ev("()=>{S.sch=[{id:'a',n:'A',ex:[]},{id:'b',n:'B',ex:[]}];S.ses=[{sc:'b',t0:Date.now()-9e5,t1:Date.now()}];S.ex=S.ex.length?S.ex:[{id:'x1',n:'Panca',g:'Petto'}];S.pl={};V.sc=null;V.scP=0;V.tab='w';render()}")
  return await u.ev("()=>[V.sc,document.querySelector('#v').innerText.includes('ultima che hai usato')]")
async def d(u):
  await u.ev("()=>{V.tab='h';render()}");await u.tap('Nascondi');t=await u.text();assert 'Benvenuto' not in t;return await u.toast()
async def e(u):
  # double tap guard
  await u.ev("()=>{V.tab='h';render()}")
  r=await u.ev("""()=>{const n=S.cd.length;const x=document.createElement('button');x.dataset.a='zz';document.body.append(x);return n}""");return r
asyncio.run(run([('card',a),('passo2',b),('preselez',c),('nascondi',d)]))
