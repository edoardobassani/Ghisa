import asyncio,subprocess,time
from playwright.async_api import async_playwright
srv=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/w',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8765/tracker-palestra.html');await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{xbAdd(['Panca piana bilanciere']);S.wc=1;V.tab='s';render()}");await pg.set_input_files('#imf','pdft/s.csv');await pg.wait_for_timeout(600)
    print('csv gym:',(await pg.evaluate("()=>!!V.im&&V.im.file")))
    await pg.evaluate("()=>{V.im=null;render()}");await pg.set_input_files('#ccf','pdft/c.csv');await pg.wait_for_timeout(600)
    print('csv cardio:',await pg.evaluate("()=>V.ci&&V.ci.L.map(x=>x.n+' '+cpTxt(cbSpec(x.B)))"))
    print(E);await b.close()
asyncio.run(m());srv.terminate()
