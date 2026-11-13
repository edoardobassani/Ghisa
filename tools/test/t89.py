# v252: Traguardi per palestra, cardio, dieta, peso e misure
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
    print(r['n'],r['L']);print(r['C'])
    ok(r['agl'] is not None,'linea di base salvata in silenzio')
    ok(not await pg.is_visible('#agun'),'nessun popup al primo avvio')
    await pg.evaluate("()=>{V.tab='tr';render()}");await pg.wait_for_timeout(300)
    ok(await pg.locator('.agi').count()==32,'32 traguardi in 5 categorie')
    ok(await pg.locator('.agi svg text').count()==0,'nessun numero nei dischi')
    await pg.screenshot(path=gb.O+'/t89a.png',full_page=True)
    await pg.locator('.agi').nth(0).click();await pg.wait_for_timeout(300)
    ok(await pg.locator('.ag4 > div').count()==5,'scheda con 5 livelli (oro compreso)')
    await pg.screenshot(path=gb.O+'/t89b.png')
    await pg.click('[data-a=agx]')
    for k in ['ckm','dpr','wob','mmi']:
      await pg.evaluate("(k)=>{V.ag=k;render()}",k);await pg.wait_for_timeout(150);await pg.screenshot(path=gb.O+'/t89_'+k+'.png')
    await pg.evaluate("()=>{V.ag=null;render()}")
    ok(await pg.locator('.aggr').count()==5,'5 sezioni')
    # sblocco: abbasso un livello visto e riapro
    await pg.evaluate("()=>{S.agl.sed=0;AGW=null;render()}");await pg.wait_for_timeout(300)
    ok(await pg.is_visible('#agun'),'popup nuovo traguardo')
    await pg.screenshot(path=gb.O+'/t89c.png')
    await pg.click('[data-a=agux]');await pg.wait_for_timeout(200)
    ok(not await pg.is_visible('#agun'),'popup chiuso')
    await pg.evaluate("()=>{document.documentElement.dataset.theme='light';V.tab='tr';render()}");await pg.wait_for_timeout(300)
    await pg.screenshot(path=gb.O+'/t89d.png',full_page=True)
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
