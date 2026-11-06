# v234: ricerca libera nel foglio «Scambia» (diario e piano pasti), grammi con le stesse kcal
import gb,asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(600)
    await pg.evaluate("()=>{const f=allF().find(f=>f.name=='Petto di pollo (crudo)');S.meal.push({id:'tm1',d:today(),m:'Pranzo',f:f.id,g:150});V.tab='n';V.nd=today();save();render()}");await pg.wait_for_timeout(300)
    await pg.click('[data-a=mpso][data-i=tm1]');await pg.wait_for_timeout(200)
    await pg.fill('#swq','tacchino');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[...document.querySelectorAll('#swres .swr b')].map(x=>x.textContent)")
    print('risultati',r)
    await pg.screenshot(path=gb.O+'swq.png')
    k0=await pg.evaluate("()=>Math.round(ln(S.meal.find(x=>x.id=='tm1')).k)")
    await pg.click('#swres [data-a=mpsw]');await pg.wait_for_timeout(300)
    x=await pg.evaluate("()=>{const x=S.meal.find(x=>x.id=='tm1');return [fo(x.f).name,x.g,Math.round(ln(x).k),x.al.length]}")
    print(k0,x)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    ok(len(r)>0 and all('acchino' in n for n in r[::2][:3]),'la ricerca trova il tacchino')
    ok('acchino' in x[0] and abs(x[2]-k0)<=k0*0.05,'scambio con kcal uguali (±5%)')
    ok(x[3]==2,'il pollo resta tra le alternative')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
