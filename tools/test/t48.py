# v209: lista della spesa come immagine PNG condivisa (API Share con file)
import asyncio,subprocess,time,os,base64
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8784','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.add_init_script("navigator.canShare=d=>!!(d&&d.files);navigator.share=async t=>{const f=t.files[0];const r=new FileReader();window.__img=await new Promise(ok=>{r.onload=()=>ok(r.result);r.readAsDataURL(f)});window.__nm=f.name}")
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8784/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;S.pf={sx:'m',age:27,act:1.55};S.h=180;S.wt=[{id:'w1',d:today(),kg:93}];V.tab='pp';V.dp={id:'sce'};render()}")
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(200)
    await pg.click('[data-a=ppv][data-v=s]');await pg.evaluate("()=>{S.spx=[{id:'x1',t:'detersivo per piatti molto lungo da tagliare forse',on:0}];document.querySelectorAll('.ppc')[0].click()}");await pg.wait_for_timeout(100)
    await pg.click('[data-a=spsh]');await pg.wait_for_timeout(100);print('scelte:',await pg.evaluate("()=>[...document.querySelectorAll('#cfm .spo b')].map(e=>e.textContent)"))
    await pg.click('#cfm [data-a=spshi]');await pg.wait_for_timeout(1500)
    d=await pg.evaluate("()=>window.__img||''");print('nome:',await pg.evaluate("()=>window.__nm"),'byte:',len(d))
    open(O+'lista-spesa.png','wb').write(base64.b64decode(d.split(',',1)[1]))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
