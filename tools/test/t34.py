import gb
import asyncio,subprocess,time
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{xbAdd(['Panca piana bilanciere']);S.wc=1;V.tab='s';V.sk='p';render()}");await pg.set_input_files('#imf','pdft/s.csv');await pg.wait_for_timeout(600)
    print('csv gym:',(await pg.evaluate("()=>!!V.im&&V.im.file")))
    await pg.evaluate("()=>{V.im=null;V.sk='c';render()}");await pg.set_input_files('#ccf','pdft/c.csv');await pg.wait_for_timeout(600)
    print('csv cardio:',await pg.evaluate("()=>V.ci&&V.ci.L.map(x=>x.n+' '+cpTxt(cbSpec(x.B)))"))
    print(E);await b.close()
asyncio.run(m())
