# v220-v221: i giorni sotto il 70% dell'obiettivo kcal non entrano nelle medie (sopra l'obiettivo contano sempre) (Home, Dieta, PDF, Excel, stima del fabbisogno)
import asyncio,subprocess,time,os,json,base64
from playwright.async_api import async_playwright
import openpyxl
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("""()=>{S.wc=1;S.goal=2000;const f=allF().find(x=>x.name=='Pane integrale');const add=(d,k)=>MPM.forEach(m=>S.meal.push({id:uid(),d,m,f:f.id,g:k/MPM.length*100/f.k}));
      [[-3,2000],[-2,500],[-1,1500],[0,2700]].forEach(([o,k])=>add(hvAdd(today(),o),k));render()}""")
    print('kcOk 2000/1400/1399/2700/4000/500:',await pg.evaluate("()=>[2000,1400,1399,2700,4000,500].map(kcOk)"))
    r=await pg.evaluate("()=>{const X=moStat(hvAdd(today(),-3),today());return [X.md,X.mx,X.kc]}");print('Riepilogo (giorni, esclusi, media):',r,'atteso [3, 1, 2067]')
    await pg.evaluate("()=>{V.tab='n';V.nd=today();V.o.dn_kc=1;render()}")
    print('Media 7 giorni:',await pg.evaluate("()=>$('#dn_kc').innerText.replace(/\\n/g,' ').slice(0,220)"))
    await pg.evaluate("()=>{V.tab='h';render()}");print('Home, riquadro kcal:',await pg.evaluate("()=>[...document.querySelectorAll('.hvtl>div')].map(x=>x.innerText.replace(/\\n/g,' ')).find(t=>t.startsWith('Kcal'))"))
    # PDF
    await pg.evaluate("()=>{V.xp='c';V.xa=hvAdd(today(),-3);V.xb=today()}")
    print('PDF:',await pg.evaluate("()=>{const d=document.createElement('div');d.innerHTML=xReport();const h=[...d.querySelectorAll('h2')].find(x=>x.textContent=='Alimentazione');return h.nextElementSibling.textContent+' | '+h.nextElementSibling.nextElementSibling.querySelector('tr:nth-child(2)').textContent}"))
    # Excel
    d=await pg.evaluate("async()=>{const bl=xmWrite(xmBook({n:1}));const u=new Uint8Array(await bl.arrayBuffer());let s='';u.forEach(x=>s+=String.fromCharCode(x));return btoa(s)}")
    open(O+'v220.xlsx','wb').write(base64.b64decode(d));wb=openpyxl.load_workbook(O+'v220.xlsx')
    rp=wb['Riepilogo'];print('Excel riquadro:',[rp.cell(r,9).value for r in (4,5,6)] if rp.cell(4,9).value else [rp.cell(r,1).value for r in (4,5,6)])
    al=wb['Alimentazione'];print('Excel «Nelle medie»:',[(al.cell(r,1).value.strftime('%d/%m'),al.cell(r,6).value,al.cell(r,12).value) for r in range(5,al.max_row+1)])
    cal=wb['Calendario kcal'];print('Excel media del calendario:',[cal.cell(r,9).value for r in range(5,cal.max_row+1)])
    # stima adattiva: 3 settimane a 2500 con pesi stabili, più 3 giorni da 1000 kcal tutti segnati: la media resta 2500
    r=await pg.evaluate("""()=>{S.meal=[];S.wt=[];S.goal=2500;const f=allF().find(x=>x.name=='Pane integrale');for(let i=24;i>=1;i--){const d=hvAdd(today(),-i),k=[5,12,18].includes(i)?1000:2500;MPM.forEach(m=>S.meal.push({id:uid(),d,m,f:f.id,g:k/MPM.length*100/f.k}));S.wt.push({id:uid(),d,kg:80})}
      AG=null;const e=adEst();return e?[e.avg,e.ex,e.td]:null}""")
    print('stima del fabbisogno (media, esclusi, fabbisogno):',r,'atteso media 2500, 3 esclusi')
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
