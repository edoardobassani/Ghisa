import asyncio
from playwright.async_api import async_playwright
JS="""(v)=>{const names=new Set();DPM.forEach(p=>JSON.stringify(p).replace(/([^",:]+):\\d+!?/g,(m,n)=>{names.add(n.trim());return m}));
 const L=[...names].map(n=>allF().find(f=>f.name==n)).filter(Boolean);return L.filter(f=>cat(f)==v).map(f=>f.name).sort().join(' | ')}"""
async def go(f,v):
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();await pg.goto('file://'+f);await pg.wait_for_timeout(500)
    r=await pg.evaluate(JS,v);await b.close();return r
a=asyncio.run(go(''+__import__('os').environ.get('PRIMA','/home/claude/w/bk/tracker-palestra-backup-v170.html')+'','Verdure'));b=asyncio.run(go('/home/claude/w/tracker-palestra.html','Verdure e ortaggi'))
A=set(a.split(' | '));B=set(b.split(' | '))
print('solo prima:',A-B);print('solo dopo:',B-A)
