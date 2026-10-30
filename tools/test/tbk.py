import asyncio,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    await pg.goto('file://'+__import__('os').environ.get('SRC','/home/claude/w/tracker-palestra.html')+'');await pg.wait_for_timeout(400)
    d=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','demo','demo_data.json')).read()
    r=await pg.evaluate("(t)=>{const x=parseBk(JSON.stringify({data:JSON.parse(t)}));norm(x.d);save();render();return S.log.length}",d)
    await pg.wait_for_timeout(300);await pg.reload();await pg.wait_for_timeout(800)
    print('ripristino backup anno intero ->',r,await pg.evaluate("()=>({log:S.log.length,meal:S.meal.length,dbm:DBM})"))
    cdp=await pg.context.new_cdp_session(pg);await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    print('ms per un tocco con salvataggio (cpu x4):',await pg.evaluate("()=>{const a=performance.now();V.tab='w';save();render();return Math.round(performance.now()-a)}"))
    await pg.evaluate("()=>{document.body.classList.add('mo');render()}");await pg.wait_for_timeout(300)
    print('menu:',await pg.evaluate("()=>{const x=[...document.querySelectorAll('nav .hint')].map(h=>h.textContent).find(t=>/Memoria|spazio/.test(t));return x||'nessun testo memoria'}"),e)
    await b.close()
asyncio.run(main())
