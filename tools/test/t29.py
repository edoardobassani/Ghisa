import asyncio
from playwright.async_api import async_playwright
D=open('/home/claude/w/demo/demo_data.json').read()
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844})
    E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(500)
    # 1) Cardio con campi scritti
    await pg.evaluate("()=>{V.tab='c';V.cdm='m';render()}");await pg.fill('#cdm','42');await pg.fill('#cdn','giro al parco');await pg.wait_for_timeout(600)
    await pg.reload();await pg.wait_for_timeout(800)
    print('cardio',await pg.evaluate("()=>[V.tab,($('#cdm')||{}).value,($('#cdn')||{}).value]"))
    # 2) Dieta con pannello aggiungi aperto e ricerca scritta
    await pg.evaluate("()=>{V.tab='n';V.mm='Pranzo';V.fsh='Pranzo';render()}");await pg.wait_for_timeout(200)
    await pg.reload();await pg.wait_for_timeout(800);print('dieta',await pg.evaluate("()=>[V.tab,V.fsh,!!document.querySelector('.fsh')]"))
    # 3) Costruttore con bozza
    await pg.evaluate("()=>{V.fsh='';V.tab='s';V.bpe={def:bpRes(bpmPB()),dk:2};render()}");await pg.fill('#bpn','Mio PB');await pg.wait_for_timeout(600)
    await pg.reload();await pg.wait_for_timeout(800);print('costr',await pg.evaluate("()=>[V.tab,!!V.bpe,V.bpe&&V.bpe.dk,($('#bpn')||{}).value]"))
    # 4) scroll in Storico palestra
    await pg.evaluate("()=>{V.bpe=null;V.tab='w';V.wv='h';render()}");await pg.evaluate("()=>scrollTo(0,900)");await pg.wait_for_timeout(700)
    await pg.reload();await pg.wait_for_timeout(1000);print('scroll',await pg.evaluate("()=>[V.tab,V.wv,scrollY]"))
    # 5) stato vecchio (13 ore) -> Home
    await pg.evaluate("()=>{const o=JSON.parse(localStorage.getItem('gymbo-view'));o.t-=13*3600e3;localStorage.setItem('gymbo-view',JSON.stringify(o));VSOK=false}");await pg.reload();await pg.wait_for_timeout(800);print('vecchio',await pg.evaluate("()=>V.tab"))
    # 6) stato rotto -> Home senza errori
    await pg.evaluate("()=>{localStorage.setItem('gymbo-view',JSON.stringify({t:Date.now(),d:today(),v:{tab:'s',bpe:{def:{n:'x'}}},f:{}}));VSOK=false}");await pg.reload();await pg.wait_for_timeout(800);print('rotto',await pg.evaluate("()=>[V.tab,!!V.bpe]"))
    # 7) seduta in corso ha la precedenza
    await pg.evaluate("()=>{V.bpe=null;V.ss={sid:'x1',sc:S.sch[0].id,fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};V.tab='ss';render();localStorage.setItem('ghisa-ss',JSON.stringify(V.ss))}");await pg.wait_for_timeout(600)
    await pg.reload();await pg.wait_for_timeout(900);print('seduta',await pg.evaluate("()=>V.tab"))
    print('errs',E);await b.close()
asyncio.run(main())
