# v244: foglio «Aggiungi a …» sopra la tastiera (spazio visibile simulato con --kb/--vvh)
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':412,'height':900},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{V.tab='n';V.mm='Colazione';V.fsh='Colazione';V.fq='';render()}");await pg.wait_for_timeout(200)
    await pg.type('#fq','pi',delay=30)
    await pg.evaluate("()=>{const R=document.documentElement.style;R.setProperty('--kb','400px');R.setProperty('--vvh','500px')}");await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const s=document.querySelector('.fsh').getBoundingClientRect(),f=document.querySelector('.fqi').getBoundingClientRect();return [Math.round(s.top),Math.round(s.bottom),Math.round(f.bottom),document.querySelectorAll('.fqi').length]}")
    print(r);ok(r[1]<=500 and r[0]>=0 and r[2]<=500,'foglio e risultati nello spazio sopra la tastiera')
    await pg.screenshot(path=gb.O+'kb.png')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
