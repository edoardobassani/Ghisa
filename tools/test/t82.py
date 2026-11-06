# v245: carico proposto senza cali ingiustificati
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
    r=await pg.evaluate("""()=>{const s=(k,r,d,rir)=>({kg:k,r,d:d||'2026-11-01',...(rir!=null?{rir}:{})});const T=(tg,ps,id)=>{const N=tgNext(tg,ps,0,ps[ps.length-1],0,id);return [N.kg,N.why]};
     const tgK={s:3,r:8,kg:60,sets:[{r:8,kg:60},{r:8,kg:60},{r:8,kg:60}]},tg0={s:3,r:8,sets:[{r:8},{r:8},{r:8}]};
     const id='tLD';S.log=S.log.filter(l=>l.e!=id);S.log.push(...[s(70,6,'2026-10-29'),s(70,6,'2026-10-29'),s(70,6,'2026-10-29')].map(x=>({...x,e:id,id:uid()})));
     return {
      kgScheda_manca1: T(tgK,[s(70,8),s(70,8),s(70,7)]),
      kgScheda_tutte: T(tgK,[s(70,8),s(70,8),s(70,8)]),
      ultimaPiuLeggera_manca: T(tg0,[s(80,8),s(80,8),s(72.5,7)]),
      ultimaPiuLeggera_tutte: T(tg0,[s(80,8),s(80,8),s(72.5,8)]),
      scheda_cambiata_dopo: T({...tgK,at:'2026-11-03',kg:75,sets:tgK.sets.map(x=>({...x,kg:75}))},[s(70,8),s(70,8),s(70,7)]),
      due_sedute_sotto: T(tg0,[s(70,6),s(70,6),s(70,5)],id),
      una_seduta_sotto: T(tg0,[s(70,6),s(70,6),s(70,5)],'altro'),
      prima_volta: T(tgK,[]),
      piramide: [0,1,2].map(j=>tgNext({s:3,r:8,sets:[{r:10,kg:50},{r:8,kg:60},{r:6,kg:70}]},[s(52.5,10),s(62.5,8),s(72.5,5)],j,null,0).kg)}}""")
    print(json.dumps(r,ensure_ascii=False))
    ok(r['kgScheda_manca1'][0]==70,'una ripetizione mancata: resta 70 (prima tornava a 60)')
    ok(r['kgScheda_tutte'][0]==72.5,'tutte fatte: +2%')
    ok(r['ultimaPiuLeggera_manca'][0]==80,'ultima serie scalata non abbassa (prima 72,5)')
    ok(r['ultimaPiuLeggera_tutte'][0]==82.5,'progressione dalla serie più pesante')
    ok(r['scheda_cambiata_dopo'][0]==75,'scheda cambiata dopo l’ultima seduta: vale la scheda')
    ok(r['due_sedute_sotto'][0]==66.25 and '−5%' in r['due_sedute_sotto'][1],'due sedute sotto: −5%')
    ok(r['una_seduta_sotto'][0]==70,'una sola seduta sotto: uguale')
    ok(r['prima_volta'][0]==60,'senza storico: carico della scheda')
    ok(r['piramide']==[52.5,62.5,72.5],'piramide: carico per serie '+str(r['piramide']))
    # nella seduta: carico e motivo a schermo
    await pg.evaluate("()=>{const sc=S.sch.find(x=>x.ex.some(e=>!isBW(e)&&S.log.some(l=>l.e==e)));V.ss={sid:'ss'+uid(),sc:sc.id,fr:0,L:[],i:sc.ex.findIndex(e=>!isBW(e)&&S.log.some(l=>l.e==e)),t0:Date.now(),d:today(),done:false};V.tab='ss';render()}");await pg.wait_for_timeout(300)
    t=await pg.evaluate("()=>[($('#ssk')||{}).value,(document.querySelector('.ldw')||{}).innerText]");print(t);ok(t[1],'motivo del carico visibile nella seduta')
    await pg.screenshot(path=gb.O+'ld.png')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
