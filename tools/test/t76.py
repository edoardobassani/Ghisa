# v239: generatore di schede su misura (domande 6-7, schede generate, blocca/⇄, riepilogo, creazione)
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    # tutte le combinazioni principali: niente errori, tempo rispettato, niente doppioni nella seduta
    R=await pg.evaluate("""()=>{const out=[];for(const go of ['f','m','t','s'])for(const n of [2,3,4,5,6])for(const min of [30,45,60,90])for(const eq of ['bmpscxen','n','sn','m']){
      const Q={go,lv:2,days:[0,1,2,3,4,5].slice(0,n),min,eqm:eq=='bmpscxen'?'a':'s',eq,zz:[],pri:['Spalle'],keep:[],ban:[],lk:{},alt:{},seed:0,cyc:6};
      const G=gnBuild(Q);const dup=G.ses.some(x=>new Set(x.it.map(y=>y.n)).size!=x.it.length);const over=Math.max(...G.ses.map(x=>x.est))-min;const empty=G.ses.some(x=>x.it.length<3);
      if(dup||(over>6&&G.ses.some(x=>x.est-min>6&&x.it.length>3))||empty)out.push([go,n,min,eq,dup,over,G.ses.map(x=>x.it.length)])}return out}""")
    print(len(R),R[:8]);ok(not R,'tutte le combinazioni: niente doppioni, sedute di almeno 3 esercizi, tempo rispettato (+6′)')
    await pg.evaluate("()=>{V.tab='s';pbOpen();V.pb.days=[0,1,3,4];V.pb.min=60;V.pb.st=6;render()}");await pg.wait_for_timeout(200)
    for g in ['Spalle','Bicipiti','Femorali e glutei']:await pg.click(f'[data-a=gpr][data-v="{g}"]')
    await pg.screenshot(path=gb.O+'gn6.png');await pg.click('[data-a=pbn]');await pg.wait_for_timeout(150)
    await pg.fill('#gkq','panca piana');await pg.wait_for_timeout(150);await pg.click('#gkr [data-v="Panca piana bilanciere"]');await pg.wait_for_timeout(150)
    await pg.fill('#gbq','stacco da');await pg.wait_for_timeout(150);await pg.click('#gbr [data-v="Stacco da terra"]');await pg.wait_for_timeout(150)
    await pg.screenshot(path=gb.O+'gn7.png');await pg.click('[data-a=gng]');await pg.wait_for_timeout(250)
    G=await pg.evaluate("()=>V.pb.G.ses.map(x=>[x.n,x.est,x.it.map(y=>[y.n,y.s,y.rg,y.why,y.w].join(' | '))])")
    for x in G:print(x[0],x[1]);[print('   ',y) for y in x[2]]
    al=[y for x in G for y in x[2]]
    ok(any(y.startswith('Panca piana bilanciere') for y in al) and not any(y.startswith('Stacco da terra') for y in al),'esercizio da tenere presente, quello escluso no')
    await pg.screenshot(path=gb.O+'gn-gen.png',full_page=True)
    k=await pg.evaluate("()=>V.pb.G.ses[0].it[2].k");n0=await pg.evaluate("()=>V.pb.G.ses[0].it[2].n")
    await pg.click(f'[data-a=gns][data-v="{k}"]');await pg.wait_for_timeout(150);n1=await pg.evaluate("()=>V.pb.G.ses[0].it[2].n");ok(n1!=n0,f'⇄ cambia esercizio: {n0} → {n1}')
    await pg.click(f'[data-a=gnl][data-v="{k}"]');await pg.wait_for_timeout(150);await pg.click('[data-a=gnr]');await pg.wait_for_timeout(150)
    n2=await pg.evaluate("()=>V.pb.G.ses[0].it[2].n");ok(n2==n1,'bloccato resta anche con «Rigenera il resto»')
    await pg.click('[data-a=gnn]');await pg.wait_for_timeout(200);await pg.screenshot(path=gb.O+'gn-sum.png',full_page=True)
    v=await pg.evaluate("()=>V.pb.G.vol");print(v)
    n=await pg.evaluate("()=>S.sch.length");await pg.click('[data-a=gnok]');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[S.sch.length,S.prog,S.pl,S.dlw]");print(r)
    ok(r[0]==n+4 and r[1]['pb']==2 and r[3]==5,'4 schede create, programma e scarico ogni 6 settimane')
    await pg.evaluate("()=>{localStorage.setItem('gb-lang','en')}");await pg.reload();await pg.wait_for_timeout(700)
    await pg.evaluate("()=>{V.tab='s';pbOpen();V.pb.days=[0,2,4];V.pb.pri=['Spalle'];V.pb.ban=['Stacco da terra'];V.pb.st='gen';render()}");await pg.wait_for_timeout(300)
    print(await pg.evaluate("()=>[...document.querySelectorAll('.gnex')].slice(0,7).map(x=>x.textContent)"));await pg.screenshot(path=gb.O+'gn-en.png',full_page=True)
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
