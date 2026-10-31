# v195: «Vedi equivalenti» nel pannello + Alimento del piano pasti
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8772','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8772/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='pp';render()}")
    await pg.click('[data-a=ppaa0][data-pm=Pranzo]');await pg.fill('#ppq','pasta di semola');await pg.wait_for_timeout(300)
    await pg.click('[data-a=ppf]');await pg.wait_for_timeout(200)
    print('compatto:',await pg.evaluate("()=>[!document.querySelector('#ppl'),!document.querySelector('#ppq'),document.querySelector('.pps b').textContent]"))
    await pg.click('[data-a=ppch]');await pg.wait_for_timeout(100)
    print('cambia:',await pg.evaluate("()=>[document.querySelector('#ppq').value,document.querySelectorAll('#ppl [data-a=ppf]').length,document.activeElement.id]"))
    await pg.click('[data-a=ppf]');await pg.wait_for_timeout(200)
    print('chiuso di default:',await pg.evaluate("()=>!document.querySelector('#ppeq').open"))
    await pg.click('#ppeq summary');await pg.wait_for_timeout(100)
    print('120? ',await pg.evaluate("()=>[...document.querySelectorAll('#ppeqb .eqr b')].map(e=>e.parentElement.textContent.trim().split('\\n')[0])"))
    await pg.fill('#ppg','80');await pg.press('#ppg','Tab');await pg.wait_for_timeout(200)
    print('80 g:',await pg.evaluate("()=>[document.querySelector('#ppeqb .hint').textContent,[...document.querySelectorAll('#ppeqb .eqr .n')].map(e=>e.textContent)]"))
    await pg.screenshot(path=O+'eq-open.png',full_page=True)
    await pg.click('#ppeqb [data-a=ppeu]');await pg.wait_for_timeout(200)
    print('dopo Usa:',await pg.evaluate("()=>[fo(V.pa.f).name,V.pa.g,document.querySelector('#ppg').value,document.querySelector('#ppeq').open]"))
    await pg.click('[data-a=ppag]');await pg.wait_for_timeout(200)
    print('nel piano:',await pg.evaluate("()=>{const d=ppD(V.pj);return d.Pranzo.map(x=>fo(x.f).name+' '+x.g)}"))
    for n,g in [('Petto di pollo (crudo)',150),('Yogurt greco 0%',150),('Mela',150),('Lenticchie lesse',200),('Olio extravergine d’oliva',10)]:
      print(n,g,'→',await pg.evaluate("([n,g])=>eqOf(allF().find(x=>x.name==n),g,4).map(o=>o.f.name+' '+o.g)",[n,g]))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
