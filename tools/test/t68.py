# v231: Crea il programma cardio per me
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.cd=[...Array(10)].map((_,i)=>({id:'c'+i,d:hvAdd(today(),-3-i*5),t:i%2?'Cyclette':'Camminata',min:40,km:5}));V.tab='s';V.sk='c';render()}")
    print('hero cardio:',await pg.evaluate("()=>$('.pbhero b').textContent"))
    await pg.click('.pbhero');print('passo 1:',await pg.evaluate("()=>[V.qc.st,V.qc.eq,qcLvOf(V.qc)]"))
    await pg.screenshot(path=O+'v231-1.png',full_page=True)
    await pg.click('[data-a=qcg][data-v=d]');await pg.click('[data-a=qcn]')
    for d in ['1','3','5']:await pg.click(f'[data-a=qcd][data-v="{d}"]')
    for d in ['0','2','4','5']:await pg.click(f'[data-a=qcd][data-v="{d}"]')
    await pg.click('[data-a=qcn]');await pg.click('[data-a=qcm][data-v="30"]');await pg.click('[data-a=qcn]')
    await pg.click('[data-a=qce][data-v=tr]');await pg.click('[data-a=qce][data-v=el]')
    await pg.screenshot(path=O+'v231-4.png',full_page=True)
    await pg.click('[data-a=qcn]');await pg.click('[data-a=qcz][data-v=gi]');await pg.click('[data-a=qcr]')
    r=await pg.evaluate("()=>V.qc.res.slice(0,5).map(r=>r.p[0]+' '+r.s+' '+r.t+' ≤'+r.mx)");print('proposte:',r)
    print('corsa tra le prime 3:',await pg.evaluate("()=>V.qc.res.slice(0,3).some(r=>qcRun(r.t))"))
    await pg.screenshot(path=O+'v231-res.png',full_page=True)
    await pg.click('.pbrc.best [data-a=qcv]');await pg.click('[data-a=qcw][data-v="1"]');await pg.screenshot(path=O+'v231-pre.png',full_page=True)
    print('accorciate:',await pg.evaluate("()=>[...document.querySelectorAll('.pbex')].map(x=>x.innerText.replace(/\\s+/g,' ')).slice(0,3)"))
    await pg.click('[data-a=qcok]');r=await pg.evaluate("()=>{const p=cpCur();return {cpr:S.cpr,ses:cpSes(p,S.cpr.pos),min:cpMin(cpSes(p,S.cpr.pos)),maxProg:Math.max(...Array.from({length:cpTot(p)},(_,i)=>cpMin(cpSes(p,i)))),cpq:S.cpq,hero:$('.pbhero b').textContent,sk:V.sk}}");print('iniziato:',r)
    await pg.evaluate("()=>{const u=$('#undo button');u&&u.click()}");await pg.wait_for_timeout(100);print('annulla:',await pg.evaluate("()=>S.cpr&&S.cpr.id"))
    # fine programma → il prossimo
    await pg.evaluate("()=>{V.qc=null;qcOpen({go:'s',lv:1,days:[1,3,5],min:45,eq:['bc'],zz:[]});V.qc.st='res';render();$('.pbrc.best [data-a=qcv]').click();$('[data-a=qcok]').click();const p=cpCur();S.cpr.pos=cpTot(p);V.tab='s';V.sk='c';render()}")
    print('fine programma:',await pg.evaluate("()=>!!$('[data-a=qcnx]')"));await pg.click('[data-a=qcnx]');print('prossimo:',await pg.evaluate("()=>[V.qc.st,V.qc.lv,V.qc.next,$('.pbq').textContent]"))
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
