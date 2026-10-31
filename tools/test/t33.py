import asyncio,subprocess,time
from playwright.async_api import async_playwright
srv=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/w',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
O='/home/claude/w/u/'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8765/tracker-palestra.html');await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{xbAdd(['Panca piana bilanciere','Lat machine','Curl manubri','Croci ai cavi']);S.wc=1;save()}")
    # gym
    await pg.evaluate("()=>{V.tab='s';render()}");await pg.set_input_files('#imf','pdft/gym_text.pdf');await pg.wait_for_timeout(1500)
    await pg.screenshot(path=O+'pdf-gym.png',full_page=True);print('gym view:',(await pg.evaluate("()=>document.querySelector('#v').innerText"))[:300].replace('\n',' | '))
    await pg.evaluate("()=>document.querySelector('[data-a=imgo][data-s=\"2\"]').click()");await pg.wait_for_timeout(200);await pg.evaluate("()=>document.querySelector('[data-a=imgo][data-s=\"3\"]').click()");await pg.wait_for_timeout(200);await pg.evaluate("()=>document.querySelector('[data-a=imok]').click()");await pg.wait_for_timeout(300)
    print('schede:',await pg.evaluate("()=>S.sch.map(s=>s.name+':'+s.ex.length)"))
    # diet
    await pg.evaluate("()=>{V.tab='pp';render()}");await pg.wait_for_timeout(200)
    await pg.set_input_files('#ipf','pdft/diet_text.pdf');await pg.wait_for_timeout(1500)
    await pg.screenshot(path=O+'pdf-diet.png',full_page=True);print('diet view:',(await pg.evaluate("()=>document.querySelector('#v').innerText"))[:400].replace('\n',' | '))
    # cardio
    await pg.evaluate("()=>{V.tab='s';V.ip=null;render()}");await pg.set_input_files('#ccf','pdft/cardio_text.pdf');await pg.wait_for_timeout(1500)
    await pg.screenshot(path=O+'pdf-cardio.png',full_page=True);print('cardio view:',(await pg.evaluate("()=>document.querySelector('#v').innerText"))[:500].replace('\n',' | '))
    await pg.evaluate("()=>{const c=document.querySelector('.cci[data-i=\"1\"]');c.click()}");await pg.wait_for_timeout(200)
    await pg.evaluate("()=>document.querySelector('[data-a=ccok]').click()");await pg.wait_for_timeout(300)
    print('csc:',await pg.evaluate("()=>[S.csc.map(c=>c.n+':'+c.t+':'+cbSpec(c.B)),S.plc,document.querySelector('#toast').textContent]"))
    # scan
    await pg.evaluate("()=>{V.tab='s';render()}");await pg.set_input_files('#ccf','pdft/scan.pdf');await pg.wait_for_timeout(1500)
    print('scan toast:',await pg.evaluate("()=>document.querySelector('#toast').textContent"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
