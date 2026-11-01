# v226: «Crea il programma per me»
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;xbAdd(['Panca piana bilanciere']);const id=S.ex[0].id;S.rm={[id]:{kg:100,src:'m',d:'2026-10-01'}};V.tab='s';render()}")
    await pg.click('[data-a=pgl]');await pg.click('[data-a=pbo]')
    await pg.screenshot(path=O+'v226-1.png',full_page=True)
    await pg.click('[data-a=pbg][data-v=m]');await pg.click('[data-a=pbn]')
    for d in ['0','2','4']: await pg.click(f'[data-a=pbd][data-v="{d}"]')   # tolgo i predefiniti
    print('<2 giorni bloccato:',await pg.evaluate("()=>{$('[data-a=pbn]').click();return V.pb.st}"))
    for d in ['0','1','3','4']: await pg.click(f'[data-a=pbd][data-v="{d}"]')
    await pg.click('[data-a=pbn]');await pg.click('[data-a=pbm][data-v="45"]');await pg.click('[data-a=pbn]')
    await pg.click('[data-a=pbem][data-v=s]')
    for c in 'bsx': await pg.click(f'[data-a=pbe][data-v={c}]')   # solo manubri, panca, cavi, elastici
    await pg.screenshot(path=O+'v226-4.png',full_page=True)
    await pg.click('[data-a=pbn]');await pg.click('[data-a=pbz][data-v=gi]');await pg.click('[data-a=pbr]')
    r=await pg.evaluate("()=>V.pb.res.slice(0,5).map(r=>r.id+' '+r.s+' miss'+(r.A?r.A.miss:'-')+' subs'+(r.A?r.A.subs.length:'-')+' ~'+r.min)");print('proposte:',r)
    await pg.screenshot(path=O+'v226-res.png',full_page=True)
    await pg.click('.pbrc.best [data-a=pbv]');await pg.wait_for_timeout(100)
    await pg.screenshot(path=O+'v226-pre.png',full_page=True)
    r=await pg.evaluate("()=>{const Q=V.pb,p=PGM.find(x=>x[0]==Q.pick),A=pbAdapt(p,Q),H=pbEq(Q);return {p:p[1],est:A.sc.map(s=>s.est),noneq:A.sc.flatMap(s=>s.it).filter(x=>!x.miss&&!atOk({name:x.n},H)).map(x=>x.n),ginocchia:A.sc.flatMap(s=>s.it).filter(x=>(ATX[x.n]||[0,''])[1].includes('gi')).map(x=>x.n),subs:A.subs.slice(0,4)}}");print('adattato:',r)
    await pg.click('[data-a=pbok]');await pg.wait_for_timeout(100)
    r=await pg.evaluate("()=>({prog:S.prog,pl:S.pl,rot:S.rot&&S.rot.sch.length,eqh:S.eqh,sch:S.sch.map(s=>s.name+':'+s.ex.length),kg:S.sch.flatMap(s=>Object.values(s.t)).flatMap(t=>t.sets).filter(x=>x.kg).length,h1:$('#v h1').textContent})");print('creato:',r)
    print('swAlt usa attrezzatura:',await pg.evaluate("()=>{V.ss={sc:S.sch[0].id,st:{},d:today()};const e=S.ex.find(x=>x.name=='Panca piana bilanciere')||S.ex[0];return swAlt(e.id).slice(0,3).map(o=>o.name+':'+o.ok)}"));await pg.evaluate('()=>{V.ss=null}')
    await pg.evaluate("()=>{const u=$('#undo button');u&&u.click()}");await pg.wait_for_timeout(100)
    print('annulla:',await pg.evaluate("()=>[S.sch.length,!!S.prog]"))
    # rinnovo
    await pg.evaluate("()=>{V.pb={...S.pbq||{},st:'res'};}")
    await pg.evaluate("()=>{V.pb=null;pbOpen({go:'m',lv:0,days:[0,2,4],min:60,eqm:'a',eq:'bmpscxen',zz:[]});V.pb.st='res';render();$('.pbrc.best [data-a=pbv]').click()}")
    print('pieno:',await pg.evaluate("()=>[V.pb.pick,[...document.querySelectorAll('.pbex small')].map(x=>x.textContent).filter(t=>/partenza/.test(t)).slice(0,2)]"))
    await pg.click('[data-a=pbok]');print('kg nelle serie:',await pg.evaluate("()=>S.sch.flatMap(s=>Object.values(s.t)).flatMap(t=>t.sets).filter(x=>x.kg).length"));await pg.evaluate("()=>{S.prog.rn='2026-01-01';V.tab='s';render()}")
    print('banner rinnovo:',await pg.evaluate("()=>!!$('.pbrw')"))
    await pg.click('[data-a=pbrw]');r=await pg.evaluate("()=>{const Q=V.pb,p=PGM.find(x=>x[0]==Q.pick),A=pbAdapt(p,Q);return [Q.st,Q.vary,A.subs.length,A.subs.slice(0,3)]}");print('rinnovo:',r)
    await pg.screenshot(path=O+'v226-rinnovo.png',full_page=True)
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
