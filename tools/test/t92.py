# v257: Modalità uscita con qualunque attività (V.cq era condiviso con «Cosa cucino»)
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
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.classList.remove('on');V.tab='c';render()}");await pg.wait_for_timeout(300)
    opts=await pg.evaluate("()=>[...document.querySelectorAll('#cdq option')].map(o=>o.value).filter(v=>v.startsWith('t:'))");print(opts)
    for v in opts:
      await pg.evaluate("()=>{V.lc=null;V.tab='c';render()}");await pg.wait_for_timeout(100)
      await pg.select_option('#cdq',v);await pg.wait_for_timeout(200)
      cc=await pg.locator('#ccov').count();btn=await pg.locator('[data-a=cdgo]').count()
      val=await pg.evaluate("()=>(document.querySelector('[data-a=cdgo]')||{dataset:{}}).dataset.v")
      if btn: await pg.click('[data-a=cdgo]');await pg.wait_for_timeout(200)
      lc=await pg.evaluate("()=>V.lc&&V.lc.t")
      ok(cc==0 and btn==1 and val==v[2:] and lc==v[2:],v+' si avvia'+('' if lc==v[2:] else ' → '+str([cc,btn,val,lc])))
    ok(await pg.evaluate("()=>V.cq==null"),'«Cosa cucino» non viene toccato')
    await pg.screenshot(path=gb.O+'/t92.png')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
