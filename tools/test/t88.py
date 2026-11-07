# v251: Traguardi (palestra, dischi a 4 livelli)
import gb,asyncio,os
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));delete S.agl;save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    r=await pg.evaluate("()=>{const C=agCalc();return {C,L:agLevel(),agl:S.agl,n:S.log.length}}")
    print(r['n'],r['L']);[print(k,v) for k,v in r['C'].items()]
    ok(r['agl'] is not None,'linea di base salvata in silenzio')
    ok(not await pg.is_visible('#agun'),'nessun popup al primo avvio')
    await pg.evaluate("()=>{V.tab='tr';render()}");await pg.wait_for_timeout(300)
    ok(await pg.locator('.agi').count()==12,'12 dischi palestra')
    ok(await pg.locator('.agi svg text').count()==0,'nessun numero nei dischi')
    await pg.screenshot(path=gb.O+'/t88a.png',full_page=True)
    await pg.locator('.agi').nth(0).click();await pg.wait_for_timeout(300)
    ok(await pg.locator('.ag4 > div').count()==4,'scheda con 4 livelli')
    await pg.screenshot(path=gb.O+'/t88b.png')
    await pg.click('[data-a=agx]')
    # sblocco: abbasso un livello visto e riapro
    await pg.evaluate("()=>{S.agl.sed=0;AGW=null;render()}");await pg.wait_for_timeout(300)
    ok(await pg.is_visible('#agun'),'popup nuovo traguardo')
    await pg.screenshot(path=gb.O+'/t88c.png')
    await pg.click('[data-a=agux]');await pg.wait_for_timeout(200)
    ok(not await pg.is_visible('#agun'),'popup chiuso')
    await pg.evaluate("()=>{document.documentElement.dataset.theme='light';V.tab='tr';render()}");await pg.wait_for_timeout(300)
    await pg.screenshot(path=gb.O+'/t88d.png',full_page=True)
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
