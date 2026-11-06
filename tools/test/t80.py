# v243: risultati della ricerca alimenti subito sotto la barra
import gb,asyncio
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':500},device_scale_factor=2,has_touch=True);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{V.tab='n';V.mm='Cena';V.fsh='Cena';V.fq='';render()}");await pg.wait_for_timeout(200)
    ok(not await pg.evaluate("()=>$('#fpre').hidden"),'a barra vuota «Recenti» e «Di solito» visibili')
    await pg.type('#fq','bir',delay=40);await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const q=$('#fq').getBoundingClientRect(),f=document.querySelector('.fqi').getBoundingClientRect();return [$('#fpre').hidden,document.querySelectorAll('.fqi').length,Math.round(f.top-q.bottom),!!document.querySelector('.fqm'),[...document.querySelectorAll('.fqn b')].map(x=>x.innerText)]}")
    print(r);ok(r[0] and r[1]<=4 and 0<=r[2]<30,'risultati subito sotto la barra, al massimo 4')
    await pg.screenshot(path=gb.O+'fq1.png')
    if r[3]:
      await pg.click('.fqm');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>document.querySelectorAll('.fqi').length")>4,'«Altri risultati» apre il resto')
    await pg.fill('#fq','');await pg.type('#fq','olio',delay=30);await pg.wait_for_timeout(200)
    q=await pg.evaluate("()=>{const b=document.querySelector('[data-a=fqa]');return b?[b.dataset.i,b.innerText]:null}");print(q);ok(q,'alimento già usato con «+ g»')
    n0=await pg.evaluate("()=>S.meal.length");await pg.click('[data-a=fqa]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[S.meal.length,S.meal[S.meal.length-1].m,V.fq,$('#fpre')&&$('#fpre').hidden]");ok(r[0]==n0+1 and r[1]=='Cena' and r[2]=='' and r[3]==False,'aggiunta con un tocco, barra svuotata '+str(r))
    await pg.type('#fq','bir',delay=30);await pg.wait_for_timeout(150);await pg.click('.fqi [data-a=fsel] >> nth=1');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[document.querySelectorAll('.fqi').length,!!$('#fg'),document.activeElement&&document.activeElement.id,!!document.querySelector('.fqbk')]");print(r);ok(r[0]==0 and r[1] and r[2]=='fg' and r[3],'scelto: solo l’alimento, grammi attivi')
    await pg.screenshot(path=gb.O+'fq2.png')
    await pg.click('.fqbk');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>document.querySelectorAll('.fqi').length")>0,'«‹ altri risultati» torna all’elenco')
    await pg.fill('#fq','');await pg.wait_for_timeout(150);ok(not await pg.evaluate("()=>$('#fpre').hidden"),'svuotando tornano «Recenti» e «Di solito»')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
