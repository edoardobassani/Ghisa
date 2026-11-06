# v240: rinnovo a fine ciclo del programma su misura (riquadro in Home, rinnovo nel generatore)
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
    await pg.evaluate("()=>{V.tab='s';pbOpen();V.pb.days=[0,1,3,4];V.pb.st='gen';render();gnDo();S.prog.start=hvAdd(today(),-42);S.prog.rn=hvAdd(today(),-1);V.tab='h';save();render()}");await pg.wait_for_timeout(300)
    t=await pg.evaluate("()=>{const c=document.querySelector('.gnrw');return c?c.innerText:''}");print(t)
    ok('ciclo è finito' in t,'riquadro del rinnovo in Home')
    await pg.locator('.gnrw').screenshot(path=gb.O+'ren-home.png')
    await pg.click('.gnrw [data-a=gnrw]');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[V.tab,V.pb&&V.pb.st,V.pb&&V.pb.ren,V.pb.G.ses.map(x=>x.it.map(y=>y.n+' | '+y.why))]");print(r[:3]);[print('  ',x) for x in r[3]]
    ok(r[1]=='gen' and r[2]==1,'«Vedi il rinnovo» apre le schede rinnovate')
    await pg.screenshot(path=gb.O+'ren-gen.png',full_page=True)
    n=await pg.evaluate("()=>S.sch.length");await pg.click('[data-a=gnn]');await pg.wait_for_timeout(150);await pg.click('[data-a=gnok]');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[S.sch.length,S.prog.start==today(),S.prog.pb]");ok(r[0]==n+4 and r[1] and r[2]==2,'rinnovo creato, nuovo ciclo da oggi')
    await pg.evaluate("()=>{V.tab='h';render()}");ok(await pg.evaluate("()=>!document.querySelector('.gnrw')"),'il riquadro sparisce')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
