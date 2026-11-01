# v229: Cardio come Palestra (Allenamento, Storico, Record) e Schede Palestra/Cardio
import asyncio,subprocess,time,os,json
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.wt=[{id:'w',d:hvAdd(today(),-1),kg:75}];S.cd=[{id:'c1',d:hvAdd(today(),-3),t:'Corsa',min:30,km:6,kc:400},{id:'c2',d:hvAdd(today(),-10),t:'Corsa',min:62,km:10.5,kc:800},{id:'c3',d:hvAdd(today(),-5),t:'Cyclette',min:40,km:15,kc:350}];V.tab='c';render()}")
    print('tabs:',await pg.evaluate("()=>[...document.querySelectorAll('.wvs button')].map(b=>b.textContent)"),'| hero:',await pg.evaluate("()=>[!!$('.shero #cdq'),$('.shero [data-a=cdgo]')&&$('.shero [data-a=cdgo]').dataset.v]"))
    print('niente più chip:',await pg.evaluate("()=>!$('.cdsc')"),'| registra a mano:',await pg.evaluate("()=>!!$('#dCdm')"),'| opzioni:',await pg.evaluate("()=>!!$('#dCop')"))
    await pg.evaluate("()=>{$('#dCdm').open=true}");await pg.fill('#cdm','25');await pg.click('[data-a=cda]');await pg.wait_for_timeout(100)
    print('salvata a mano:',await pg.evaluate("()=>S.cd.length"));await pg.evaluate('()=>{cfClose()}')
    await pg.click('[data-a=cdv][data-v=h]');print('storico:',await pg.evaluate("()=>[$('.hsg').textContent,document.querySelectorAll('details.hsx').length,$('details.hsx[open] .cdsd')!=null]"))
    await pg.click('details.hsx[open] [data-a=cde]');print('modifica aperta:',await pg.evaluate("()=>!!$('#cem')"))
    await pg.click('[data-a=cdv][data-v=r]');print('record:',await pg.evaluate("()=>[...document.querySelectorAll('.rmr')].map(r=>r.innerText.replace(/\\s+/g,' ')).slice(0,5)"))
    await pg.click('[data-a=cdv][data-v=a]');await pg.select_option('#cdq','t:Cyclette');print('scelta cyclette:',await pg.evaluate("()=>[V.cq,$('[data-a=cdgo]').dataset.v]"))
    await pg.click('[data-a=cdgo]');print('dal vivo:',await pg.evaluate("()=>V.lc&&V.lc.t"))
    await pg.evaluate("()=>{V.lc=null;lcKeep();V.tab='s';V.sk='c';render()}")
    print('schede cardio:',await pg.evaluate("()=>[!!$('[data-a=skk][data-v=c].on'),!!$('[data-a=cpl]'),$('#v').innerText.includes('Schede cardio')]"))
    await pg.click('[data-a=skk][data-v=p]');print('schede palestra senza cardio:',await pg.evaluate("()=>!$('#v').innerText.includes('Schede cardio')"))
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
