# v249: quantità della spesa modificabili e dispensa proiettata sulle settimane future
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.dsp=null;S.spq={};S.spx=[];S.mc={};save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("""()=>{const a=n=>allF().find(f=>f.name==n).id,w=hvMon(today()),w2=hvAdd(w,7),day=(L)=>({Pranzo:L.map((x,i)=>({id:'q'+Math.random(),gid:'g',f:a(x[0]),g:x[1]}))});
      const P={};for(let d=0;d<7;d++)P[d]=day([['Pasta di semola (cruda)',100],['Yogurt greco 0%',170],['Zucchine',200]]);S.mpw[w]=JSON.parse(JSON.stringify(P));S.mpw[w2]=JSON.parse(JSON.stringify(P));
      dsPut(a('Pasta di semola (cruda)'),1000);V.pw=w;V.tab='sp';V.spv='s';V.psd=null;render()}""")
    await pg.wait_for_timeout(300)
    yid=await pg.evaluate("()=>allF().find(f=>f.name=='Yogurt greco 0%').id")
    r=await pg.evaluate(f"()=>[!!document.querySelector('[data-a=spqe][data-i=\"{yid}\"]'),document.querySelector('#v').innerText.includes('Già in casa')]");ok(all(r),'quantità toccabile, pasta già in casa '+str(r))
    await pg.click(f'[data-a=spqe][data-i="{yid}"]');await pg.wait_for_timeout(150)
    await pg.screenshot(path=gb.O+'sq1.png',full_page=True)
    v0=await pg.evaluate("()=>$('#spqg').value");await pg.click('.spqed [aria-label="Più"]');v1=await pg.evaluate("()=>$('#spqg').value");print(v0,v1);ok(int(v1)-int(v0)==125,'+ di un vasetto')
    await pg.click('.spqed .cxc button >> nth=1');await pg.click('[data-a=spqs]');await pg.wait_for_timeout(200)
    r=await pg.evaluate(f"()=>[S.spq[V.pw]['{yid}'],document.querySelector('[data-a=spqe][data-i=\"{yid}\"]').className,spText()]");print(r[0]);ok(r[0]['g']>0 and 'ed' in r[1],'quantità salvata e in viola');ok(str(r[0]['g']) in r[2].replace('.','') or 'vasett' in r[2],'testo condiviso con la quantità modificata')
    # il piano cambia
    await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;Object.values(S.mpw[V.pw]).forEach(D=>D.Pranzo.find(x=>x.f==a('Yogurt greco 0%')).g=300);render()}");await pg.wait_for_timeout(200)
    ok(await pg.evaluate("()=>!!document.querySelector('.spdr')"),'avviso: il piano è cambiato')
    await pg.screenshot(path=gb.O+'sq2.png',full_page=True)
    await pg.click('.spdr [data-a=spqk]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>!document.querySelector('.spdr')"),'«Tieni» toglie l’avviso')
    # 0 = non serve, poi rimetti
    zid=await pg.evaluate("()=>allF().find(f=>f.name=='Zucchine').id")
    await pg.click(f'[data-a=spqe][data-i="{zid}"]');await pg.fill('#spqg','0');await pg.click('[data-a=spqs]');await pg.wait_for_timeout(200)
    r=await pg.evaluate(f"()=>[!document.querySelector('[data-a=spqe][data-i=\"{zid}\"]'),!!$('#spns')]");ok(all(r),'0 → «Non serve»')
    await pg.evaluate("()=>{V.o.spns=true;render()}");await pg.click(f'#spns [data-a=spqr][data-i="{zid}"]');await pg.wait_for_timeout(150);ok(await pg.evaluate(f"()=>!!document.querySelector('[data-a=spqe][data-i=\"{zid}\"]')"),'«Rimetti»')
    # ho fatto la spesa usa la quantità modificata
    r=await pg.evaluate(f"()=>{{S.mc['{yid}']=1;const q=S.spq[V.pw]['{yid}'].g;dsBought();return [q,Math.round(dsLeft('{yid}'))]}}");ok(r[0]==r[1],'«Ho fatto la spesa» mette la quantità modificata '+str(r))
    # altro da comprare con quantità
    await pg.evaluate("()=>{S.spx=[{id:'xx1',t:'Caffè macinato',on:false}];render()}");await pg.click('[data-a=spxe][data-i=xx1]');await pg.fill('#spxq','2 pacchi');await pg.click('[data-a=spxs]');await pg.wait_for_timeout(150)
    ok(await pg.evaluate("()=>S.spx[0].q=='2 pacchi'&&spText().includes('Caffè macinato – 2 pacchi')"),'quantità libera negli articoli a mano')
    # proiezione: settimana prossima con 150 g di pasta
    r=await pg.evaluate("""()=>{const a=n=>allF().find(f=>f.name==n).id,pid=a('Pasta di semola (cruda)');S.dsp.it[pid].q=dsLeft(pid);S.dsp.it[pid].t=Date.now()-1;S.meal=S.meal.filter(x=>x.d!=today());DSC=null;
      const left=dsLeft(pid),w=hvMon(today()),days=7-((new Date().getDay()+6)%7);S.dsp.it[pid].q=100*days+50;DSC=null;V.pw=hvAdd(w,7);const {o,HC}=spAll();return [days,o[pid]?[o[pid].g,o[pid].hv,o[pid].pj]:null,HC.includes(pid)]}""")
    print(r);ok(r[1] and r[1][2]==1 and abs(r[1][1]-50)<1,'settimana prossima: «ne avrai circa 50 g»')
    await pg.evaluate("()=>{V.spqe=null;render()}");await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>document.querySelector('#v').innerText.includes('ne avrai circa')"),'scritta «ne avrai circa»')
    await pg.screenshot(path=gb.O+'sq3.png',full_page=True)
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
