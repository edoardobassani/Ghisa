# v256: micronutrienti della settimana del piano pasti, collegati a Integratori
import gb,asyncio,os
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl=null;save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.classList.remove('on')}")
    # crea il piano con il generatore e confermalo
    r=await pg.evaluate("()=>{V.tab='pp';mgOpen();const Q=V.mg;Q.G=mgBuild(Q);mgDo();save();render();return {pv:V.pv,w:V.pw,has:!!S.mpw[V.pw]}}")
    await pg.wait_for_timeout(400);print(r)
    ok(r['pv']=='w' and r['has'],'dopo la conferma si apre la vista settimana')
    ok(await pg.locator('#pmc').count()==1,'card micronutrienti della settimana')
    ok(await pg.locator('#pmc .pmr').count()==10,'10 righe (fibre + 9 micronutrienti)')
    P=await pg.evaluate("()=>{const P=pmW(V.pw);return {nd:P.nd,cov:P.cov,rows:P.rows.map(x=>[x.n,Math.round(x.p),x.st,x.low])}}");print(P)
    y=await pg.evaluate("()=>document.querySelector('#pmc').getBoundingClientRect().top");ok(abs(y)<160,'scorre sul riepilogo ('+str(round(y))+')')
    await pg.locator('#pmc').screenshot(path=gb.O+'/t91a.png')
    low=[x for x in P['rows'] if x[2]=='low' and x[0] in('Vitamina D','Calcio','Magnesio','Zinco','Ferro','Vitamina B12','Potassio')]
    ok(len(low)>0,'almeno una carenza integrabile: '+str([x[0] for x in low]))
    nm=low[0][0];k=await pg.evaluate("(n)=>pmW(V.pw).rows.find(x=>x.n==n).sk",nm)
    await pg.click(f'#pmc [data-a=itg][data-k={k}]');await pg.wait_for_timeout(200)
    ok(await pg.locator(f'#itd_{k}').count()==1,'campo dose dopo «Lo prendo già»')
    st=await pg.evaluate("(n)=>pmW(V.pw).rows.find(x=>x.n==n).st",nm);ok(st=='nd','senza dose resta da sistemare ('+st+')')
    need=await pg.evaluate("(n)=>{const x=pmW(V.pw).rows.find(x=>x.n==n);return Math.ceil((100-x.p)/100*x.r)}",nm)
    await pg.fill(f'#itd_{k}',str(need));await pg.click(f'[data-a=itds][data-k={k}]');await pg.wait_for_timeout(200)
    st=await pg.evaluate("(n)=>{const x=pmW(V.pw).rows.find(x=>x.n==n);return [x.st,Math.round(x.p+x.sp)]}",nm);ok(st[0]=='sup' and st[1]>=99,'con la dose risulta coperto '+str(st))
    ok(await pg.locator('#pmc .pmb i.s').count()==1,'segmento integratore nella barra')
    await pg.locator('#pmc').screenshot(path=gb.O+'/t91b.png')
    # dose oltre il massimo
    if k in('vd','ca','zn','fe','mg'):
      await pg.fill(f'#itd_{k}','99999');await pg.click(f'[data-a=itds][data-k={k}]');await pg.wait_for_timeout(200)
      ok(await pg.locator('#pmc .itw').count()==1,'avviso oltre il massimo EFSA')
      await pg.fill(f'#itd_{k}',str(need));await pg.click(f'[data-a=itds][data-k={k}]');await pg.wait_for_timeout(200)
    # vista giorno: avviso compatto
    await pg.evaluate("()=>{V.pv='p';render()}");await pg.wait_for_timeout(200)
    ok(await pg.locator('.pmh').count()==1,'avviso compatto nella vista giorno')
    await pg.screenshot(path=gb.O+'/t91c.png')
    await pg.click('.pmh');await pg.wait_for_timeout(300);ok(await pg.evaluate("()=>V.pv")=='w','dall’avviso si apre la settimana')
    # Integratori: dose e riga del piano
    await pg.evaluate("()=>{V.tab='it';render()}");await pg.wait_for_timeout(300)
    ok(await pg.locator(f'#itd_{k}').count()==1,'dose anche in Integratori')
    ok('Nel piano pasti di questa settimana' in await pg.inner_text('main, body'),'Integratori cita il piano')
    await pg.screenshot(path=gb.O+'/t91d.png',full_page=True)
    # senza diario: Integratori usa il piano
    r=await pg.evaluate("()=>{const m=S.meal;S.meal=[];FC=null;const D=itData(),L=itList(D);const t=document.createElement('div');S.meal=m;return {n:D.n,pl:!!D.pl,ks:L.filter(o=>/piano pasti/.test(o.why||'')).map(o=>o.k)}}");print(r)
    ok(r['n']==0 and r['pl'] and len(r['ks'])>0,'senza diario i consigli usano il piano')
    await pg.evaluate("(k)=>{V.tab='pp';V.pv='w';render()}",k);await pg.wait_for_timeout(200)
    await pg.click(f'#pmc [data-a=itg][data-k={k}]');await pg.wait_for_timeout(200)
    ok(await pg.evaluate("(k)=>!S.itg[k]&&!(S.itd||{})[k]",k),'«Non lo prendo più» toglie integratore e dose')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
