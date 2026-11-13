# v260: GPS del telefono nella Modalità uscita
import gb,asyncio,json,math
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
dd=json.loads(D);RT=[list(map(float,x.split(','))) for x in [c for c in dd['cd'] if c.get('rte') and c['t']=='Corsa'][0]['rte'].split(';')]
def hav(a,b):
  R=6371000;t=math.pi/180;dl=(b[0]-a[0])*t;dn=(b[1]-a[1])*t;x=math.sin(dl/2)**2+math.cos(a[0]*t)*math.cos(b[0]*t)*math.sin(dn/2)**2;return 2*R*math.asin(min(1,math.sqrt(x)))
# punti ogni secondo lungo il percorso a 4,17 m/s (4′00″/km)
pts=[];acc=0;i=0;pos=RT[0];v=1000/240
seg=[(RT[k],RT[k+1],hav(RT[k],RT[k+1])) for k in range(len(RT)-1)]
def at(s):
  for a,b,l in seg:
    if s<=l:f=s/l if l else 0;return [a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f]
    s-=l
  return RT[-1]
tot=sum(l for _,_,l in seg);print('percorso m',round(tot))
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,permissions=['geolocation'],geolocation={'latitude':RT[0][0],'longitude':RT[0][1],'accuracy':5})
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl=null;save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.remove();V.tab='c';V.cdsel='t:Corsa';render()}");await pg.wait_for_timeout(1500)
    ok(await pg.locator('[data-a=gpt]').count()==1,'interruttore GPS per la corsa')
    await pg.evaluate("()=>render()");await pg.wait_for_timeout(300)
    st=await pg.inner_text('#gps');print(st);ok('GPS pronto' in st,'stato «GPS pronto» dal GPS vero (simulato dal browser)')
    await pg.screenshot(path=gb.O+'/t95a.png')
    await pg.select_option('#cdq','t:Tapis roulant');await pg.wait_for_timeout(200);ok(await pg.locator('[data-a=gpt]').count()==0,'niente GPS per il tapis roulant')
    await pg.select_option('#cdq','t:Corsa');await pg.wait_for_timeout(200)
    # orologio finto per simulare l'uscita
    await pg.evaluate("()=>{window.__t=Date.now();Date.now=()=>window.__t}")
    await pg.click('[data-a=cdgo]');await pg.wait_for_timeout(200)
    ok(await pg.evaluate("()=>!!(V.lc&&V.lc.g)"),'uscita partita con il GPS')
    feed=[]
    t=0;s=0
    for k in range(600):  # 10 minuti di corsa
      t+=1;s+=v;q=at(s);feed.append([t,q[0],q[1],5])
      if k==100:feed.append([t+.5,q[0]+0.01,q[1],5])   # salto impossibile di 1 km
      if k==200:feed.append([t+.5,q[0],q[1]+0.0005,60]) # punto impreciso
    stop=at(s)
    for k in range(40):  # 40 s fermo al semaforo, con il GPS che balla di 1–2 m
      t+=1;feed.append([t,stop[0]+(k%3-1)*0.00001,stop[1]+((k+1)%3-1)*0.00001,6])
    for k in range(240): # riparte, altri 4 minuti
      t+=1;s+=v;q=at(s);feed.append([t,q[0],q[1],5])
    T0=await pg.evaluate("()=>window.__t")
    r=await pg.evaluate("""(F)=>{const t0=window.__t,log=[];F.forEach(([t,la,lo,ac])=>{window.__t=t0+t*1000;gpFeed({coords:{latitude:la,longitude:lo,accuracy:ac,altitude:120},timestamp:window.__t});const q=V.lc;if(q.pa&&q.apa&&!log.length)log.push(t)});const q=V.lc,g=q.g;return {d:Math.round(g.d),sp:g.sp,el:Math.round(lcEl(q)),ap:log,pa:q.pa,P:q.P.length}}""",feed)
    print(r)
    exp=v*840
    ok(abs(r['d']-exp)/exp<.03,f"distanza {r['d']} m (attesi ~{round(exp)})")
    ok(len(r['sp'])==3 and all(225<=x<=255 for x in r['sp']),'intertempi a ogni km intorno a 4′00″: '+str(r['sp']))
    ok(len(r['ap'])==1 and 600<r['ap'][0]<=615,'pausa automatica al semaforo')
    ok(r['pa']==0 and r['P']>=1,'ripartita da sola dopo la pausa')
    ok(abs(r['el']-(t-(r['P'] and 30)))<=20,'tempo attivo senza la sosta: '+str(r['el'])+' s su '+str(t))
    await pg.evaluate("()=>render()");await pg.wait_for_timeout(200)
    tx=await pg.inner_text('main');ok('Distanza' in tx and 'Passo ora' in tx and 'Km 3' in tx,'riquadri dal vivo: distanza, passo, intertempi')
    ok(await pg.locator('#gpm svg').count()==1,'percorso disegnato dal vivo')
    await pg.screenshot(path=gb.O+'/t95b.png',full_page=True)
    await pg.click('[data-a=gplk]');await pg.wait_for_timeout(200)
    ok(await pg.locator('#lcpk.on').count()==1,'schermo «in tasca» attivo')
    await pg.screenshot(path=gb.O+'/t95c.png')
    await pg.click('#lcpk div >> nth=0');await pg.wait_for_timeout(200);ok(await pg.locator('#lcpk.on').count()==1,'un tocco non lo sblocca')
    box=await pg.locator('#lcun').bounding_box();await pg.mouse.move(box['x']+40,box['y']+40);await pg.mouse.down();await pg.wait_for_timeout(1400);await pg.mouse.up();await pg.wait_for_timeout(200)
    ok(await pg.locator('#lcpk.on').count()==0,'tenendo premuto si sblocca')
    await pg.click('[data-a=lce]');await pg.wait_for_timeout(200)
    km=await pg.input_value('#lckm');ok(km.replace(',','.')[:3]==str(round(exp/1000,2))[:3],'km del GPS già scritti: '+km)
    await pg.click('[data-a=lcs]');await pg.wait_for_timeout(300)
    o=await pg.evaluate("()=>{const c=S.cd[S.cd.length-1];return {km:c.km,gps:c.gps,n:(c.rte||'').split(';').length,sp:c.sp,from:c.from,asc:c.asc,elv:(c.elv||[]).length,src:c.src}}");print(o)
    ok(o['gps']==1 and o['n']>50 and len(o['sp'])==3 and o['from']=='GPS telefono','salvata con percorso, intertempi e fonte')
    await pg.evaluate("()=>{V.tab='h';render()}");await pg.wait_for_timeout(1300)
    ok(await pg.evaluate("()=>GP.w==null"),'GPS spento uscendo dal Cardio dopo il salvataggio')
    # unione con il file dell'orologio
    u=await pg.evaluate("()=>{const c=S.cd[S.cd.length-1];const D=gxDup({st:c.st+20000,t1:c.st+600000,d:c.d,sel:c.t});return !!(D&&D.live&&D.c.id==c.id)}");ok(u,'il file dell’orologio della stessa uscita si unisce a questa')
    # permesso negato
    ok(await pg.evaluate("()=>{GP.err='deny';return gpStatH().includes('Posizione negata')}"),'messaggio se la posizione è negata')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
