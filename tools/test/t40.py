# v199: riquadro della fotocamera del codice a barre sempre visibile; «Scansiona di nuovo»; senza fotocamera un messaggio nella cornice
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8776','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
FAKE="""window.__n=0;window.BarcodeDetector=class{constructor(){}async detect(){window.__n++;return window.__n%12==0?[{rawValue:'8001234567897'}]:[]}}"""
VIS="()=>{const f=document.querySelector('#bco .bcf'),v=document.querySelector('#bcv'),r=f.getBoundingClientRect();return {frame:getComputedStyle(f).display!='none'&&r.height>50,video:getComputedStyle(v).display!='none',off:f.classList.contains('off'),msg:document.querySelector('#bcm').textContent,again:!document.querySelector('#bcr').hidden,form:!!document.querySelector('#bq_n')}}"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    ctx=await b.new_context(viewport={'width':390,'height':844},permissions=['camera']);await ctx.add_init_script(FAKE)
    await ctx.route('**/world.openfoodfacts.org/**',lambda r:r.fulfill(json={'status':1,'product':{'product_name':'Biscotti prova','brands':'Marca','nutriments':{'energy-kcal_100g':450,'proteins_100g':7,'carbohydrates_100g':70,'fat_100g':15}}}))
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8776/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;bcOpen()}");await pg.wait_for_timeout(1200)
    print('in scansione:',await pg.evaluate(VIS))
    await pg.wait_for_timeout(3500)
    print('dopo lettura:',await pg.evaluate(VIS));await pg.screenshot(path=O+'bc-letto.png',full_page=True)
    await pg.click('#bcr');await pg.wait_for_timeout(300)
    print('scansiona di nuovo:',await pg.evaluate(VIS))
    await pg.wait_for_timeout(3500);print('seconda lettura:',await pg.evaluate("()=>window.__n>=24")," ",await pg.evaluate(VIS))
    await pg.fill('#bcc','80012345');await pg.click('#bcg');await pg.wait_for_timeout(500)
    print('codice a mano:',await pg.evaluate(VIS))
    await pg.click('#bcx');print('chiuso, fotocamera spenta:',await pg.evaluate("()=>!document.querySelector('#bco')&&!BC.st"))
    # senza fotocamera
    c2=await b.new_context(viewport={'width':390,'height':844});await c2.add_init_script("delete window.BarcodeDetector")
    p2=await c2.new_page();await p2.goto('http://127.0.0.1:8776/'+os.path.basename(SRC));await p2.wait_for_timeout(800)
    await p2.evaluate("()=>{S.wc=1;bcOpen()}");await p2.wait_for_timeout(600)
    print('senza lettore:',await p2.evaluate(VIS),await p2.evaluate("()=>document.querySelector('#bcph').textContent"));await p2.screenshot(path=O+'bc-off.png')
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
