# v225: import dello storico da Strong e Hevy (file di prova in test/hi)
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True);D=os.path.dirname(os.path.abspath(__file__))+'/hi/'
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;xbAdd(['Panca piana bilanciere']);const id=S.ex[0].id;S.log.push({id:'pre',d:'2026-06-01',e:id,kg:50,r:5});V.tab='x';render()}")
    print('scheda d\'ingresso:',await pg.evaluate("()=>[$('#v h1').textContent,!!$('#hif')]"))
    await pg.set_input_files('#hif',D+'strong.csv');await pg.wait_for_timeout(400)
    r=await pg.evaluate("()=>{const H=V.hi;return {app:H.app,ses:H.S.length,unit:H.unit,E:Object.values(H.E).map(e=>e.en+' → '+e.m.k+':'+(e.m.it||'')+' ('+e.v+')')}}");print('Strong:',r)
    print('doppioni:',await pg.evaluate("()=>[...hiDupSet()]"))
    await pg.screenshot(path=O+'v225-anteprima.png',full_page=True)
    # cambio un abbinamento e importo
    await pg.select_option('select.hims[data-en="Belt Squat"]','x:Squat')
    await pg.click('[data-a=hiok]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const imp=S.ses.filter(s=>s.src=='strong');return {sedute:imp.length,serie:S.log.filter(l=>imp.some(s=>s.id==l.ss)).length,cardio:S.cd.filter(c=>c.src=='strong').length,schede:S.sch.map(s=>s.name+':'+s.ex.length),nuovi:S.ex.map(e=>e.name).filter(n=>/Landmine|Single|Incline/.test(n)),toast:$('#toast').textContent}}");print('dopo import:',r)
    r=await pg.evaluate("()=>{const s=S.ses.find(s=>s.src=='strong');const L=S.log.filter(l=>l.ss==s.id);return {d:s.d,dur:Math.round((s.t1-s.t0)/60000),nt:s.nt,prima:L.slice(0,3).map(l=>nm(l.e)+' '+l.kg+'x'+l.r+(l.rir!=null?' rir'+l.rir:'')),riscaldamento:L.some(l=>l.kg==30)}}");print('prima seduta:',r)
    print('plank in secondi:',await pg.evaluate("()=>S.log.filter(l=>nm(l.e).startsWith('Plank')).slice(0,1).map(l=>l.r)"))
    print('storico:',await pg.evaluate("()=>[...document.querySelectorAll('.hsx summary b')].slice(0,2).map(x=>x.textContent)"))
    await pg.screenshot(path=O+'v225-storico.png')
    # annulla
    await pg.evaluate("()=>{const u=$('#undo button');u&&u.click()}");await pg.wait_for_timeout(100)
    print('annulla:',await pg.evaluate("()=>(S.ses||[]).filter(s=>s.src=='strong').length"))
    # Hevy
    await pg.evaluate("()=>{V.tab='x';render()}");await pg.set_input_files('#hif',D+'hevy.csv');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>{const H=V.hi;return {app:H.app,ses:H.S.length,unit:H.unit,E:Object.values(H.E).map(e=>e.en+' → '+e.m.k+':'+(e.m.it||''))}}");print('Hevy:',r)
    await pg.click('#hiwu');await pg.click('[data-a=hiok]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const imp=S.ses.filter(s=>s.src=='hevy');const L=S.log.filter(l=>imp.some(s=>s.id==l.ss));return {sedute:imp.length,serie:L.length,durata:Math.round((imp[0].t1-imp[0].t0)/60000),rir:L.filter(l=>l.rir!=null).map(l=>l.rir)[0],cardio:S.cd.filter(c=>c.src=='hevy').map(c=>c.t+' '+c.min+'min '+c.km+'km')[0],schede:S.sch.map(s=>s.name)}}");print('Hevy importato (con riscaldamento):',r)
    # file sbagliato
    await pg.evaluate("()=>hiOpen('a;b;c\\n1;2;3','x.csv')");print('file sbagliato:',await pg.evaluate("()=>$('#toast').textContent"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
