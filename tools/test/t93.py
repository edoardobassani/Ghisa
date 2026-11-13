# v259: stesso percorso dal GPS, velocità a parità di battito, Forma aerobica
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl=null;save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.remove()}")
    # corse sullo stesso giro con passo che migliora e battito che scende; una al contrario; una su un altro giro
    r=await pg.evaluate("""()=>{const base=S.cd.find(c=>c.t=='Corsa'&&c.rte);const P=base.rte.split(';');S.cd=S.cd.filter(c=>!(c.t=='Corsa'&&c.rte));
     const mk=(d,min,hr,rev,shift)=>{let pts=P.map(x=>x.split(',').map(Number));if(rev)pts=pts.reverse();if(shift)pts=pts.map(([a,b])=>[a+shift,b]);S.cd.push({id:uid(),d,t:'Corsa',min,km:7.41,hr:{a:hr,m:hr+8},asc:40,rte:pts.map(([a,b])=>a.toFixed(5)+','+b.toFixed(5)).join(';'),src:'file'})};
     [['2026-09-06',32,156],['2026-09-13',31.8,155],['2026-09-27',31.3,154],['2026-10-04',31.2,153],['2026-10-11',31,154],['2026-10-25',30.4,152]].forEach(([d,mi,hr])=>mk(d,mi,hr));
     mk('2026-11-07',30.2,151,1);mk('2026-11-01',33,150,0,.02);save();RTGC=null;const G=rtGroups();return {gr:G.G.map(g=>g.length),last:S.cd.filter(c=>c.d=='2026-11-07'&&c.t=='Corsa').map(c=>c.id)[0]}}""")
    print(r);ok(sorted(r['gr'])==[1,7] or sorted(r['gr'])[-1]==7,'7 corse riconosciute sullo stesso giro (anche al contrario), quella spostata di 2 km no')
    await pg.evaluate("(id)=>cdSumOpen(id)",r['last']);await pg.wait_for_timeout(300)
    t=await pg.inner_text('#cfm');ok('Sullo stesso percorso' in t and 'più veloce a parità di battito' in t,'riepilogo con stesso percorso e confronto a parità di battito')
    ok(await pg.locator('#cfm .rtt tr').count()==7,'tabella con le ultime 6 volte')
    ok(await pg.locator('#cfm .rtt tr.best.cur').count()==1,'la più veloce è evidenziata (è questa)')
    await pg.click('#cfm [data-a=rtn]');await pg.wait_for_timeout(150);await pg.fill('#rtni','Giro del parco');await pg.click('#cfm [data-a=rtns]');await pg.wait_for_timeout(200)
    t=await pg.inner_text('#cfm');ok('Giro del parco' in t,'nome del percorso salvato')
    await pg.locator('#cfm').screenshot(path=gb.O+'/t93a.png')
    await pg.evaluate("()=>{const m=document.querySelector('#cfm');if(m)m.remove()}")
    # Forma aerobica nei Record
    await pg.evaluate("()=>{V.lc=null;V.tab='c';V.cv='r';render()}");await pg.wait_for_timeout(300)
    ok(await pg.locator('.fasv circle').count()>=8,'grafico Forma aerobica con i punti')
    t=await pg.inner_text('main');ok('Forma aerobica' in t and 'A parità di' in t,'riassunto Forma aerobica')
    await pg.screenshot(path=gb.O+'/t93b.png',full_page=False)
    # senza dati sufficienti
    n=await pg.evaluate("()=>{const k=S.cd;S.cd=S.cd.filter(c=>c.t!='Corsa');const h=faCard();S.cd=k;return h.includes('almeno 5 uscite')}");ok(n,'messaggio quando mancano le uscite')
    # confronto semplice (senza GPS) mostra la riga a parità di battito
    s=await pg.evaluate("()=>{const a={id:'x1',d:'2026-11-02',t:'Bici',min:60,km:24,hr:{a:130,m:140}},c={id:'x2',d:'2026-11-09',t:'Bici',min:60,km:25,hr:{a:128,m:139}};S.cd.push(a,c);const h=cdSumH(c);S.cd=S.cd.filter(x=>x.id!='x1'&&x.id!='x2');return h.includes('A parità di battito')}");ok(s,'riga a parità di battito anche senza GPS')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
