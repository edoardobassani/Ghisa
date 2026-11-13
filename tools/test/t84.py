# v247: Spesa e dispensa come sezione a sé
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.click('#mb');await pg.wait_for_timeout(200)
    t=await pg.evaluate("()=>[...document.querySelectorAll('nav [data-t]')].map(x=>x.dataset.t+':'+x.innerText.trim())");print(t)
    ok(any(x.startswith('sp:') for x in t),'voce nel menu')
    await pg.click('nav [data-t=sp]');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[V.tab,document.querySelector('#v h1').innerText,!!document.querySelector('[data-a=spv][data-v=d]')]");print(r);ok(r[0]=='sp' and 'Spesa e dispensa' in r[1] and r[2],'sezione con Spesa | Dispensa')
    await pg.screenshot(path=gb.O+'sp1.png')
    await pg.click('[data-a=spv][data-v=d]');await pg.wait_for_timeout(200);ok(await pg.evaluate("()=>!!$('#dsq')"),'scheda Dispensa')
    await pg.screenshot(path=gb.O+'sp2.png')
    await pg.evaluate("()=>{V.tab='pp';render()}");await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[...document.querySelectorAll('.pvt button')].map(x=>x.innerText)");print(r);ok('Spesa' not in r and 'Dispensa' not in [x.split('•')[0].strip() for x in r],'Piano pasti senza Spesa e Dispensa')
    await pg.click('.skrow[data-a=spgo]');await pg.wait_for_timeout(200);ok(await pg.evaluate("()=>V.tab=='sp'&&V.spv=='s'"),'collegamento da Piano pasti')
    t=await pg.evaluate("()=>($('#nbb')||{}).innerText||''");print(t);ok('Piano pasti' in t,'«indietro» torna a Piano pasti')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
