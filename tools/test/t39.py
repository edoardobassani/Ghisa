# v198: «Svuota la settimana» nel piano pasti (conferma, settimane successive, Annulla)
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8775','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8775/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.tab='pp';V.dp={id:'sce'};render()}")
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(200)
    # copia nelle 2 settimane dopo
    await pg.evaluate("()=>{const W=hvMon(today());[7,14].forEach(n=>S.mpw[hvAdd(W,n)]=mpClone(S.mpw[W]));render()}")
    st="()=>{const W=hvMon(today());return [0,7,14,21].map(n=>{const k=hvAdd(W,n);return Math.round([0,1,2,3,4,5,6].reduce((t,d)=>t+MP.reduce((a,m)=>a+((mpGet(k)[d]||{})[m]||[]).reduce((s,x)=>s+ln(x).k,0),0),0))})}"
    print('prima:',await pg.evaluate(st))
    await pg.click('[data-a=ppsv0]');await pg.wait_for_timeout(100)
    print('dialogo:',await pg.evaluate("()=>document.querySelector('#cfm').innerText.replace(/\\n+/g,' | ')"))
    await pg.screenshot(path=O+'sv-dlg.png')
    await pg.click('#cfm [data-a=ppsv]');await pg.wait_for_timeout(200)
    print('solo questa:',await pg.evaluate(st),await pg.evaluate("()=>document.querySelector('#toast').textContent"))
    await pg.click('#undo button');await pg.wait_for_timeout(200);print('annulla:',await pg.evaluate(st))
    await pg.click('[data-a=ppsv0]');await pg.check('#ppsvf');await pg.click('#cfm [data-a=ppsv]');await pg.wait_for_timeout(200)
    print('anche le successive:',await pg.evaluate(st),await pg.evaluate("()=>[document.querySelector('#toast').textContent,!!S.dpa,document.querySelector('[data-a=ppsv0]').disabled]"))
    await pg.screenshot(path=O+'sv-after.png',full_page=True)
    # aggiungo qualcosa e verifico che la settimana dopo resti vuota
    await pg.evaluate("()=>{const f=allF().find(x=>x.name=='Mela');ppD(0).Spuntino.push({id:'z1',gid:'z1',f:f.id,g:150});save();render()}")
    print('aggiunta lunedì:',await pg.evaluate(st))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
