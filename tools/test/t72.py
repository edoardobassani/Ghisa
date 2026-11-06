# v235: età in un riquadro suo in Obiettivi e misure, prima del sesso
import gb,asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(600)
    await pg.evaluate("()=>{V.tab='o';render();scrollTo(0,0)}");await pg.wait_for_timeout(200)
    o=await pg.evaluate("()=>{const a=document.querySelector('.agc'),s=document.querySelector('.sxc:not(.agc)');return [!!a,!!s&&!!(a.compareDocumentPosition(s)&4),document.querySelectorAll('#tda').length]}")
    await pg.fill('#tda','34');await pg.press('#tda','Tab');await pg.wait_for_timeout(200)
    age=await pg.evaluate("()=>S.pf.age");await pg.screenshot(path=gb.O+'eta.png')
    await pg.evaluate("()=>{document.querySelectorAll('details').forEach(d=>d.open=true)}")
    rif=await pg.evaluate("()=>[...document.querySelectorAll('#v p.hint')].map(p=>p.textContent).find(t=>t.startsWith('Età:'))||''")
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    ok(o[0] and o[1],'riquadro Età prima del Sesso');ok(o[2]==1,'un solo campo età nella pagina');ok(age==34,'età salvata');ok('34' in rif,'nel fabbisogno resta il richiamo: '+rif)
    await pg.evaluate("()=>{localStorage.setItem('gb-lang','en')}");await pg.reload();await pg.wait_for_timeout(600);await pg.evaluate("()=>{V.tab='o';render()}");await pg.wait_for_timeout(200)
    en=await pg.evaluate("()=>document.querySelector('.agc').textContent.replace(/\\s+/g,' ')");print(en)
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
