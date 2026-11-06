import gb
import asyncio
from playwright.async_api import async_playwright
from t import SEED
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(400);await pg.evaluate(SEED)
    await pg.evaluate("()=>{for(let i=0;i<300;i++)S.cd.push({id:'z'+i,d:dShift(today(),-i),t:'Corsa',min:30,km:5});save()}");await pg.reload();await pg.wait_for_timeout(500)
    await pg.evaluate("()=>{V.tab='s';V.o.dSch=true;render()}");await pg.wait_for_timeout(200)
    b1=await pg.query_selector('[data-a=scdup]');await (await b1.evaluate_handle("e=>e.closest('.card')")).as_element().screenshot(path='dup1.png')
    await pg.click('[data-a=scdup]');await pg.wait_for_timeout(300)
    print(await pg.evaluate("()=>[S.sch.map(s=>s.name+':'+s.ex.length),V.ed==S.sch[1].id,document.querySelector('#undo span').textContent]"))
    await pg.screenshot(path='dup2.png')
    await pg.click('#undo button');await pg.wait_for_timeout(200);print('undo',await pg.evaluate("()=>S.sch.length"))
    await pg.click('[data-a=scdup]');await pg.wait_for_timeout(200);await pg.evaluate("()=>{V.ed='';render()}");await pg.click('[data-a=scdup] >> nth=0');print(await pg.evaluate("()=>S.sch.map(s=>s.name)"))
    await pg.evaluate("()=>{V.tab='c';V.cv='h';render()}");R="()=>document.querySelectorAll('details.hsx').length";print('righe',await pg.evaluate(R),await pg.evaluate("()=>(document.querySelector('[data-a=cdmore]')||{}).textContent"))
    while await pg.evaluate("()=>!!document.querySelector('[data-a=cdmore]')"):
      await pg.click('[data-a=cdmore]')
    print('righe dopo «Mostra altre»:',await pg.evaluate(R),await pg.evaluate("()=>S.cd.length"))
    print(e);await b.close()
asyncio.run(main())
