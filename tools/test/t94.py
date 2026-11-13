# v259: generatore del piano pasti, «Copri i micronutrienti»
import gb,asyncio,time
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl=null;save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.remove();V.tab='pp';mgOpen();render()}");await pg.wait_for_timeout(200)
    ok(await pg.evaluate("()=>V.mg.mi===1"),'opzione attiva di serie')
    R=[]
    for seed in range(8):
      r=await pg.evaluate("(s)=>{const Q=V.mg;Q.seed=s;const t0=performance.now(),G=mgBuild(Q),ms=performance.now()-t0,G0=mgBuild0({...Q});const L=miL();const lo=(a)=>a.map((v,j)=>j>0&&v<80?L[j][0]:null).filter(Boolean);return {ms:Math.round(ms),sw:G.mi.sw.length,b0:lo(G.mi.b0),b1:lo(G.mi.b1),k0:Math.round(G0.av.k),k1:Math.round(G.av.k),p0:Math.round(G0.av.p),p1:Math.round(G.av.p),tg:[G.tg.K,G.tg.P],d0:G.mi.b0.map(Math.round),d1:G.mi.b1.map(Math.round),na:[Math.round(G.mi.b0[0]),Math.round(G.mi.b1[0])],fish:[0,1].map(z=>(z?G:G0).W.reduce((t,D)=>t+MP.reduce((u,m)=>u+(D[m]||[]).filter(y=>y.r=='pm'&&(mgRow('pm',y.n)||[])[5]=='f').length,0),0)),why:G.W.flatMap(D=>MP.flatMap(m=>(D[m]||[]).filter(y=>/^al posto/.test(y.why||'')).map(y=>y.n+' · '+y.why))).slice(0,3)}}",seed)
      R.append(r);print(r)
    ok(all(r['sw']<=6 for r in R),'al massimo 6 cambi')
    ok(all(len(r['b1'])<=len(r['b0']) for r in R),'mai più carenze di prima')
    ok(all(all(r['d1'][j]>=80 or r['d0'][j]<80 for j in range(1,9)) for r in R),'nessun nutriente coperto finisce sotto l’80%')
    ok(all(abs(r['k1']-r['tg'][0])/r['tg'][0]<.06 for r in R),'calorie sempre sull’obiettivo')
    ok(all(r['p1']>=r['tg'][1]*.9 for r in R),'proteine sempre sull’obiettivo')
    ok(all(r['fish'][1]-r['fish'][0]<=2 for r in R),'al massimo 2 porzioni di pesce in più')
    ok(all(r['na'][1]<=max(100,r['na'][0]) for r in R),'il sodio non sale oltre il limite')
    ok(any(r['sw']>0 for r in R),'almeno un piano con cambi')
    ok(max(r['ms'] for r in R)<1500,'tempo di calcolo '+str(max(r['ms'] for r in R))+' ms')
    s=[i for i,r in enumerate(R) if r['sw']>0][0]
    await pg.evaluate("(s)=>{const Q=V.mg;Q.seed=s;Q.st=4;const G=mgBuild(Q);Q.di=G.mi.sw[0].days[0];render()}",s);await pg.wait_for_timeout(300)
    st=await pg.evaluate("()=>V.mg.st");print('st',st)
    ok(await pg.locator('.gnex small.mi').count()>0,'motivo del cambio sotto l’alimento')
    await pg.screenshot(path=gb.O+'/t94a.png',full_page=True)
    await pg.click('[data-a=mgsu]');await pg.wait_for_timeout(300)
    ok(await pg.locator('.mgmir').count()>0 and await pg.locator('.mgsw div').count()>0,'media della settimana con prima/dopo e lista dei cambi')
    await pg.screenshot(path=gb.O+'/t94b.png',full_page=True)
    # blocco e ⇄ rispettati
    r=await pg.evaluate("()=>{const Q=V.mg,G=mgBuild(Q),k=G.mi.sw[0].k,from=G.mi.sw[0].from,parts=k.split('.');Q.lk[k]=from;const G2=mgBuild(Q);const ok1=!G2.mi.sw.some(o=>o.k==k);delete Q.lk[k];Q.alt[k]=1;const G3=mgBuild(Q);const ok2=!G3.mi.sw.some(o=>o.k==k);delete Q.alt[k];return [ok1,ok2]}")
    ok(r[0] and r[1],'alimento bloccato o cambiato a mano non viene toccato')
    # opzione spenta = come prima
    r=await pg.evaluate("()=>{const Q=V.mg;Q.mi=0;const a=JSON.stringify(mgBuild(Q).W.map(D=>MP.map(m=>(D[m]||[]).map(y=>y.n+y.g)))),b=JSON.stringify(mgBuild0(Q).W.map(D=>MP.map(m=>(D[m]||[]).map(y=>y.n+y.g))));Q.mi=1;return a==b}")
    ok(r,'con l’opzione spenta il piano è identico a prima')
    await pg.evaluate("()=>{V.mg.st=3;render()}");await pg.wait_for_timeout(200)
    ok(await pg.locator('#mgmi').count()==1,'casella «Copri i micronutrienti» nelle opzioni')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
