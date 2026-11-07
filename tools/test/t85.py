# v248: «Cosa cucino con quello che ho?» e alimento aperto
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.dsp=null;S.mfo={};S.mpg=null;S.meal=S.meal.filter(x=>x.d!=today());save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("""()=>{const a=n=>{const f=allF().find(f=>f.name==n);if(!f)throw n;return f.id};const t=today();
      [['Riso basmati (crudo)',1000],['Petto di pollo (crudo)',400],['Spinaci',300,dShift(t,1)],['Uovo intero',360],['Zucchine',600],['Patate',1000],['Ricotta vaccina',250,dShift(t,3)],['Pane integrale',400],['Pasta di semola (cruda)',500],['Passata di pomodoro',700],['Tonno al naturale',240]].forEach(x=>{try{dsPut(a(x[0]),x[1],x[2])}catch(e){console.log('manca '+e)}});
      S.goal=2000;S.meal.push({id:uid(),d:t,m:'Colazione',f:a('Fiocchi d’avena'),g:80},{id:uid(),d:t,m:'Pranzo',f:a('Pasta di semola (cruda)'),g:90});save();V.tab='n';V.nd=t;render()}""")
    await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[...document.querySelectorAll('.cck')].map(x=>x.dataset.pm)");print(r);ok('Cena' in r,'pulsante sui pasti vuoti di oggi')
    await pg.click('.cck[data-pm=Cena]');await pg.wait_for_timeout(400)
    r=await pg.evaluate("()=>{const c=V.cq,B=c.B;return [B.N,B.R.slice(0,3).map(x=>[x.title,x.t.k,x.t.p,x.mins,x.L.map(y=>y.f.name+' '+y.g).join(', ')]),B.R.length]}")
    print(json.dumps(r,ensure_ascii=False,indent=0))
    N=r[0];T=r[1]
    ok(len(T)==3,'tre proposte');ok(abs(T[0][1]-N['K'])/N['K']<.12,'calorie vicine al residuo');ok(T[0][2]>=N['P']*.85,'proteine vicine al residuo')
    ok(any('spinaci' in x[0].lower() for x in T[:2]),'usa prima gli spinaci in scadenza')
    await pg.screenshot(path=gb.O+'cc1.png')
    await pg.click('[data-a=cchow][data-v="0"]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>document.querySelectorAll('.ccs li').length")>=3,'«Come si fa»')
    await pg.click('[data-a=ccfl][data-v=n]');await pg.wait_for_timeout(200);r=await pg.evaluate("()=>V.cq.B.R.slice(0,3).map(x=>[x.title,x.mins])");print(r);ok(r and all(x[1]==0 for x in r),'filtro senza fornelli')
    await pg.click('[data-a=ccfl][data-v=""]');await pg.wait_for_timeout(200)
    n0=await pg.evaluate("()=>S.meal.length");await pg.click('[data-a=ccadd][data-v="0"]');await pg.wait_for_timeout(400)
    r=await pg.evaluate("()=>[S.meal.length,S.meal.filter(x=>x.d==today()&&x.m=='Cena').length,!V.cq,($('#dstst')||{}).innerText]");print(r);ok(r[1]>=3 and r[2],'aggiunto a cena')
    await pg.screenshot(path=gb.O+'cc2.png')
    k=await pg.evaluate("()=>S.food.length");await pg.click('[data-a=ccrc]');await pg.wait_for_timeout(200);ok(await pg.evaluate(f"()=>S.food.length=={k}+1&&!!S.food[S.food.length-1].rc"),'salvato come ricetta')
    # annulla da nuovo
    await pg.evaluate("()=>{S.meal=S.meal.filter(x=>!(x.d==today()&&x.m=='Cena'));render()}");await pg.click('.cck[data-pm=Cena]');await pg.wait_for_timeout(300);await pg.click('[data-a=ccadd][data-v="1"]');await pg.wait_for_timeout(300)
    await pg.click('[data-a=ccun]');await pg.wait_for_timeout(200);ok(await pg.evaluate("()=>S.meal.filter(x=>x.d==today()&&x.m=='Cena').length")==0,'Annulla toglie il pasto')
    # dispensa: «Cosa cucino adesso?» e aperto
    await pg.evaluate("()=>{V.tab='sp';V.spv='d';render()}");await pg.wait_for_timeout(200);ok(await pg.evaluate("()=>!!document.querySelector('#v .cck')"),'«Cosa cucino adesso?» in Dispensa')
    pid=await pg.evaluate("()=>allF().find(f=>f.name=='Passata di pomodoro').id")
    await pg.click(f'[data-a=dse0][data-i="{pid}"]');await pg.wait_for_timeout(150);await pg.click('[data-a=dsop]');await pg.wait_for_timeout(150)
    r=await pg.evaluate(f"()=>[S.dsp.it['{pid}'].op,S.dsp.it['{pid}'].ex,dShift(today(),4)]");ok(r[0] and r[1]==r[2],'aperto: scade fra 4 giorni '+str(r))
    await pg.screenshot(path=gb.O+'cc3.png',full_page=True)
    await pg.click(f'[data-a=dse0][data-i="{pid}"]');await pg.wait_for_timeout(100)
    if not await pg.evaluate("()=>!!$('[data-a=dsop]')"):
      await pg.click(f'[data-a=dse0][data-i="{pid}"]');await pg.wait_for_timeout(100)
    await pg.click('[data-a=dsop]');await pg.wait_for_timeout(150);r=await pg.evaluate(f"()=>[S.dsp.it['{pid}'].op||null,S.dsp.it['{pid}'].ex||null]");ok(not r[0] and not r[1],'annullare «aperto» rimette com’era '+str(r))
    # colazione / spuntino
    r=await pg.evaluate("()=>{S.meal=S.meal.filter(x=>!(x.d==today()&&x.m=='Colazione'));const a=n=>allF().find(f=>f.name==n).id;dsPut(a('Fiocchi d’avena'),400);dsPut(a('Latte parz. scremato'),1000);dsPut(a('Banana'),600);dsPut(a('Yogurt greco 0%'),500);return [ccBuild('Colazione',{}).R.slice(0,2).map(x=>x.title+' '+x.t.k),ccBuild('Spuntino',{}).R.slice(0,2).map(x=>x.title+' '+x.t.k)]}");print(r);ok(r[0] and r[1],'colazione e spuntino')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
