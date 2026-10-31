# v208: lista della spesa condivisa come link (#spesa=…): creazione, apertura su un altro telefono, spunte salvate lì
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';B='http://127.0.0.1:8783/'+os.path.basename(SRC)
srv=subprocess.Popen(['python3','-m','http.server','8783','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});await ctx.add_init_script("navigator.share=t=>{window.__sh=t;return Promise.resolve()}")
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(B);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.tab='pp';V.dp={id:'sce'};render()}")
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(200)
    await pg.click('[data-a=ppv][data-v=s]');await pg.evaluate("()=>{document.querySelectorAll('.ppc')[0].click()}");await pg.wait_for_timeout(100)
    await pg.evaluate("()=>{S.spx=[{id:'x1',t:'detersivo',on:0}];render()}")
    await pg.click('[data-a=spsh]');await pg.wait_for_timeout(100);print('scelte:',await pg.evaluate("()=>[...document.querySelectorAll('#cfm .spo b')].map(e=>e.textContent)"))
    await pg.screenshot(path=O+'shl-scelta.png')
    await pg.click('#cfm [data-a=spshl]');await pg.wait_for_timeout(400)
    sh=await pg.evaluate("()=>window.__sh");u=sh['url'];print('link:',u[:60]+'…','lunghezza',len(u),'| testo:',sh['text'])
    h=u[u.index('#'):]
    c2=await b.new_context(viewport={'width':390,'height':844});p2=await c2.new_page();E2=[];p2.on('pageerror',lambda e:E2.append(str(e)))
    await p2.goto(B+h);await p2.wait_for_timeout(1200)
    print('altro telefono:',await p2.evaluate("()=>[V.tab,document.querySelector('#v h1').textContent,[...document.querySelectorAll('#v .spc h2')].map(e=>e.textContent).join(', '),document.querySelectorAll('.shlc').length]"))
    await p2.evaluate("()=>{document.querySelectorAll('.shlc')[0].click();document.querySelectorAll('.shlc')[3].click()}");await p2.wait_for_timeout(150)
    await p2.screenshot(path=O+'shl-aperto.png',full_page=True)
    await p2.reload();await p2.wait_for_timeout(1200)
    print('dopo ricarica:',await p2.evaluate("()=>[document.querySelector('.spbar').textContent,document.querySelectorAll('.shlc:checked').length]"))
    print('dati del primo telefono non toccati:',await p2.evaluate("()=>S.meal.length+S.food.length==0||'?'"))
    await p2.click('[data-a=shlx]');await p2.wait_for_timeout(200);print('apri Gym-Bo:',await p2.evaluate("()=>[V.tab,location.hash]"))
    print('errori',E,E2);await b.close()
asyncio.run(m());srv.terminate()
