# v223: sezione Informazioni (gratuità, licenza PolyForm Noncommercial, versione ufficiale, fonti) e avvisi in Benvenuto, Guida, PDF, Excel, immagini
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    print('commento con la licenza nel sorgente:',await pg.evaluate("()=>[...document.childNodes].concat([...document.documentElement.childNodes]).some(n=>n.nodeType==8&&n.textContent.includes('Required Notice'))"))
    print('Benvenuto:',await pg.evaluate("()=>{V.tab='h';render();return ($('.wcc .hint')||{}).textContent}"))
    await pg.click('#mb');await pg.wait_for_timeout(250)
    print('voce nel menu (gruppo Dati):',await pg.evaluate("()=>{const b=$('nav [data-t=inf]');let e=b,g='';while(e=e.previousElementSibling){if(e.classList.contains('nvg')){g=e.textContent;break}}return [b.textContent,g]}"))
    await pg.click('nav [data-t=inf]');await pg.wait_for_timeout(200)
    print('pagina:',await pg.evaluate("()=>[...document.querySelectorAll('#v h2')].map(x=>x.textContent)"))
    print('link:',await pg.evaluate("()=>[...document.querySelectorAll('#v a')].map(a=>a.href+' '+a.target)"))
    await pg.screenshot(path=O+'v223-info.png',full_page=True)
    print('Guida:',await pg.evaluate("()=>{V.tab='r';render();const d=$('#gr_gratis');return d?d.querySelector('summary').textContent:'manca'}"))
    print('PDF:',await pg.evaluate("()=>{const d=document.createElement('div');d.innerHTML=xReport();return d.querySelector('.ft').textContent.slice(0,90)}"))
    print('errori',E);await b.close()
asyncio.run(m())
