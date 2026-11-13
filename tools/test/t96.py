# v261: livello oro (quinto livello) nei Traguardi
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl=null;save()}",D);await pg.reload();await pg.wait_for_timeout(900)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.classList.remove('on')}")
    r=await pg.evaluate("()=>({n5:AGG.filter(g=>g[4].length==5).length,n4:AGG.filter(g=>g[4].length==4).map(g=>g[0]),inc:AGG.every(g=>g[4].every((t,i)=>!i||t>g[4][i-1])),pts:AGP[4]})")
    print(r);ok(r['n5']==44 and r['n4']==['wob'],'oro su tutti i traguardi tranne l’obiettivo di peso (che arriva al 100%)')
    ok(r['inc'],'soglie crescenti');ok(r['pts']==1000,'1000 punti per l’oro')
    # forzo alcuni livelli d'oro
    await pg.evaluate("()=>{const C=agCalc();['sed','stc','ckm'].forEach(k=>{const g=AGG.find(x=>x[0]==k);C[k]={x:g[4][4],lv:5}});const g=AGG.find(x=>x[0]=='stk');C.stk={x:g[4][3]+10,lv:4};AGW=AGC.k;V.tab='tr';render()}");await pg.wait_for_timeout(300)
    ok(await pg.locator('.agi small.gd').count()==4,'«oro» sotto i traguardi d’oro (3 forzati + 1 già preso nei dati demo)')
    ok(await pg.locator('.agi svg path[fill="var(--ag5b)"]').count()==4,'scintilla sui dischi d’oro')
    t=await pg.inner_text('main');ok('di 220 livelli' not in t and 'livello 4 di 5' in t,'«livello N di 5»')
    await pg.screenshot(path=gb.O+'/t96a.png',full_page=True)
    await pg.evaluate("()=>{V.ag='stk';render()}");await pg.wait_for_timeout(200)
    ok(await pg.locator('.ag4 > div').count()==5,'scheda con 5 livelli');t=await pg.inner_text('#agov');ok('Oro' in t and 'All’oro mancano' in t,'scheda: oro grigio e quanto manca: '+t.split('All’oro mancano')[-1][:30].strip())
    await pg.locator('#agov .xps').screenshot(path=gb.O+'/t96b.png')
    await pg.evaluate("()=>{V.ag='sed';render()}");await pg.wait_for_timeout(200);t=await pg.inner_text('#agov');ok('livello oro' in t,'scheda completata: «livello oro»')
    await pg.evaluate("()=>{V.ag=null;S.agl.stc=4;AGW=null;agWatch()}");await pg.wait_for_timeout(300)
    t=await pg.inner_text('#agun');ok('traguardo d’oro' in t.lower() and '+1000 punti' in t,'avviso «Traguardo d’oro»')
    await pg.locator('#agun .agub').screenshot(path=gb.O+'/t96c.png')
    await pg.click('[data-a=agux]')
    # tema chiaro
    await pg.evaluate("()=>{document.documentElement.dataset.theme='light';render()}");await pg.wait_for_timeout(200)
    c=await pg.evaluate("()=>getComputedStyle(document.documentElement).getPropertyValue('--ag5').trim()");ok(c=='#a68216','oro più scuro nel tema chiaro')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
