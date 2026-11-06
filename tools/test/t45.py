# v206: riepilogo dell'uscita cardio (dopo il salvataggio e dallo storico), confronto con l'uscita simile precedente
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("""()=>{S.wc=1;const d0=hvAdd(today(),-7),d1=hvAdd(today(),-3);
      S.cd.push({id:'c1',d:d0,t:'Corsa',min:30,km:5,kc:380,hr:{a:152,m:171},hz:[1,6,15,7,1]});
      S.cd.push({id:'c2',d:d1,t:'Corsa',min:28.5,km:5.1,kc:375,hr:{a:148,m:169},hz:[1,8,14,5,0.5],asc:42});
      S.cd.push({id:'c3',d:d1,t:'Cyclette',min:45,km:18,kc:300});V.tab='c';V.cv='r';render()}""")
    await pg.evaluate("()=>document.querySelector('[data-a=cdsum][data-i=c2]').click()");await pg.wait_for_timeout(200)  # dai Record
    print('riepilogo c2:',await pg.evaluate("()=>document.querySelector('#cfm').innerText.replace(/\\n+/g,' | ')"))
    await pg.screenshot(path=O+'cs-sum.png')
    await pg.click('#cfm [data-a=cfx]')
    await pg.evaluate("()=>cdSumOpen('c3')");print('cyclette:',await pg.evaluate("()=>document.querySelector('#cfm').innerText.replace(/\\n+/g,' | ')"))
    await pg.click('#cfm [data-a=cfx]')
    # salvataggio manuale: si apre da solo
    await pg.evaluate("()=>{V.cv='a';V.o.dCdm=true;V.cdm='m';render()}");await pg.fill('#cdm','25');await pg.click('[data-a=cda]');await pg.wait_for_timeout(200)
    print('dopo il salvataggio a mano si apre il riepilogo:',await pg.evaluate("()=>!document.querySelector('#cfm').hidden&&document.querySelector('#cfm').innerText.split('\\n')[0]"))
    print('errori',E);await b.close()
asyncio.run(m())
