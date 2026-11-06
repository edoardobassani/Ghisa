# v236: silhouette dei gruppi muscolari con muscoli disegnati e richiami (numero e nome)
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w);E=[]
    for l in ['it','en']:
      pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);pg.on('pageerror',lambda e:E.append(str(e)))
      await pg.add_init_script(f"if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','{l}')")
      await pg.goto(gb.URL);await pg.wait_for_timeout(500)
      await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
      await pg.evaluate("()=>{V.tab='g';V.mv='s';V.mp='4';render();document.querySelectorAll('#v details').forEach(d=>d.open=true)}");await pg.wait_for_timeout(300)
      sv=pg.locator('svg[role=img][aria-label*=ilhouette]')
      n=await sv.count();ok(n==1,f'[{l}] silhouette presente')
      t=await sv.evaluate("s=>[s.querySelectorAll('path').length,[...s.querySelectorAll('text')].map(x=>x.textContent)]")
      print(t[1]);ok(t[0]>40 and len(t[1])>=10,f'[{l}] muscoli disegnati e 9 richiami')
      await sv.screenshot(path=gb.O+f'sil-{l}.png')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
