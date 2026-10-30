import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    await pg.goto('file://'+__import__('os').environ.get('SRC','/home/claude/w/tracker-palestra.html')+'');await pg.wait_for_timeout(400)
    await pg.evaluate("()=>{xbAdd(['Squat','Panca piana bilanciere']);save()}");await pg.wait_for_timeout(200);await pg.reload();await pg.wait_for_timeout(400)
    print('prima',await pg.evaluate("()=>S.ex.length"))
    await pg.evaluate("()=>{const b=document.createElement('button');b.dataset.a='wipe2';document.body.append(b);b.click();document.querySelector('#wpq').value='CANCELLA';document.querySelector('#wpq').dispatchEvent(new Event('input',{bubbles:true}));const w=document.querySelector('#wpb3');w.disabled=false;w.click()}")
    await pg.wait_for_timeout(2000)
    print('dopo cancella',await pg.evaluate("()=>({ex:S.ex.length,dbm:DBM,keys:Object.keys(localStorage)})"),e)
    await b.close()
asyncio.run(main())
