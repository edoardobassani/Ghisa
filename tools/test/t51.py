# v212: avvisi fuori dall'app (notifica a fine recupero e a cambio fase del cardio guidato), striscia per attivarli
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
INIT="""window.__N=[];window.__hid=false;Object.defineProperty(document,'visibilityState',{get:()=>window.__hid?'hidden':'visible'});
const RN=window.Notification;window.Notification=function(t,o){window.__N.push(t+' | '+(o&&o.body||''))};window.Notification.permission='default';window.Notification.requestPermission=()=>{window.Notification.permission='granted';return Promise.resolve('granted')};"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});await ctx.add_init_script(INIT)
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;xbAdd(['Panca piana bilanciere']);const id=S.ex[0].id;S.sch.push({id:'sx',name:'Prova',ex:[id],t:{[id]:{s:3,r:8}},rt:{[id]:90}});V.tab='w';render()}")
    await pg.evaluate("()=>{const b=document.querySelector('[data-a=ssg]');b&&b.click()}");await pg.wait_for_timeout(200)
    if not await pg.evaluate("()=>V.tab=='ss'"):
      await pg.evaluate("()=>{V.ss={sid:'ss1',sc:'sx',fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};V.tab='ss';render()}")
    print('striscia:',await pg.evaluate("()=>(document.querySelector('.ntb')||{}).innerText||'nessuna'"))
    await pg.screenshot(path=O+'ntf-ban.png')
    await pg.click('[data-a=ntfa]');await pg.wait_for_timeout(200)
    print('dopo Attiva:',await pg.evaluate("()=>[S.ntf,(document.querySelector('.ntl')||{}).textContent,!!BGA]"))
    await pg.evaluate("()=>{tStart(2);window.__hid=true}");await pg.wait_for_timeout(2800)
    print('fine recupero (app in sottofondo):',await pg.evaluate("()=>window.__N"))
    await pg.evaluate("()=>{window.__hid=false;window.__N=[];tStart(1)}");await pg.wait_for_timeout(1800)
    print('app in primo piano, nessuna notifica:',await pg.evaluate("()=>window.__N"))
    # cardio guidato con fasi brevi
    await pg.evaluate("()=>{V.ss=null;V.cs={sc:'',scn:'Prova',sp:'',F:[{k:'S',s:2},{k:'W',s:2,i:'F'},{k:'D',s:1}],t:'Corsa',t0:Date.now(),pt:0,pa:0,sk:0,ci:null};V.tab='cs';render();window.__hid=true;window.__N=[]}");await pg.wait_for_timeout(6500)
    print('cardio guidato:',await pg.evaluate("()=>window.__N"))
    await pg.evaluate("()=>{window.__hid=false;csClose();render()}");print('suono di sottofondo spento a fine sessione:',await pg.evaluate("()=>BGA===null"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
