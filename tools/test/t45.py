# v206: riepilogo dell'uscita cardio (dopo il salvataggio e dallo storico), confronto con l'uscita simile precedente
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8781','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8781/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("""()=>{S.wc=1;const d0=hvAdd(today(),-7),d1=hvAdd(today(),-3);
      S.cd.push({id:'c1',d:d0,t:'Corsa',min:30,km:5,kc:380,hr:{a:152,m:171},hz:[1,6,15,7,1]});
      S.cd.push({id:'c2',d:d1,t:'Corsa',min:28.5,km:5.1,kc:375,hr:{a:148,m:169},hz:[1,8,14,5,0.5],asc:42});
      S.cd.push({id:'c3',d:d1,t:'Cyclette',min:45,km:18,kc:300});V.tab='c';V.o.dCd=true;render()}""")
    await pg.evaluate("()=>document.querySelector('[data-a=cdsum][data-i=c2]').click()");await pg.wait_for_timeout(200)
    print('riepilogo c2:',await pg.evaluate("()=>document.querySelector('#cfm').innerText.replace(/\\n+/g,' | ')"))
    await pg.screenshot(path=O+'cs-sum.png')
    await pg.click('#cfm [data-a=cfx]')
    await pg.evaluate("()=>cdSumOpen('c3')");print('cyclette:',await pg.evaluate("()=>document.querySelector('#cfm').innerText.replace(/\\n+/g,' | ')"))
    await pg.click('#cfm [data-a=cfx]')
    # salvataggio manuale: si apre da solo
    ok=await pg.evaluate("()=>{const t=document.querySelector('#cdt'),m=document.querySelector('#cdm')||document.querySelector('#cdv');return !!t}")
    print('form manuale presente:',ok)
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
