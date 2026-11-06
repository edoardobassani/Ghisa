# v207: lettura al tocco su peso (Riepilogo Home), altitudine e battito, sulla demo di un anno (costruita al volo da tools/demo/make-demo.py)
import gb,os,subprocess,sys
subprocess.run([sys.executable,gb.REPO+'/tools/demo/make-demo.py'],env={**os.environ,'SRC':gb.SRC,'DEMO_OUT':gb.D+'/demo.html'},check=True,stdout=subprocess.DEVNULL)
import asyncio
from playwright.async_api import async_playwright
S=gb.D+'/'
async def tap(pg,sel,frac):
  el=await pg.query_selector(sel);await el.scroll_into_view_if_needed();b=await el.bounding_box();x=b['x']+b['width']*frac;y=b['y']+b['height']/2
  await pg.mouse.move(x,y);await pg.mouse.down();await pg.wait_for_timeout(80);await pg.mouse.up()
  return await pg.evaluate("s=>{const e=document.querySelector(s);return e.classList.contains('on')?e.querySelector('.tst').textContent:'(niente)'}",sel)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file://'+S+'demo.html');await pg.wait_for_timeout(1500)
    await pg.evaluate("()=>{V.tab='h';render()}");await pg.wait_for_timeout(300)
    print('peso inizio:',await tap(pg,'.wksw .tsc',0.02),' fine:',await tap(pg,'.wksw .tsc',0.98))
    await pg.screenshot(path=S+'ts-home.png')
    await pg.evaluate("()=>{V.tab='c';V.cv='h';S.cd.forEach(c=>V.o['cdh_'+c.id]=true);render();const d=[...document.querySelectorAll('details.gxd')].find(x=>x.querySelectorAll('.tsc').length>=2)||document.querySelector('details.gxd');d.open=true;V.o[d.id]=true;window.__d=d.id}");await pg.wait_for_timeout(300)
    did=await pg.evaluate("()=>window.__d")
    n=await pg.evaluate("id=>document.querySelectorAll('#'+id+' .tsc').length",did);print('grafici nella scheda:',n)
    for k in range(n):
      print(' grafico',k,':',await tap(pg,f'#{did} .tsc:nth-of-type(1)' if False else f'#{did} >> nth=0',0) if False else '')
    labs=await pg.evaluate("id=>[...document.querySelectorAll('#'+id+' .tsc')].map((e,i)=>{e.id='tsx'+i;return e.id})",did)
    for l in labs:print(l,'a metà:',await tap(pg,'#'+l,0.5))
    await pg.screenshot(path=S+'ts-cardio.png')
    print('errori',E);await b.close()
asyncio.run(m())
