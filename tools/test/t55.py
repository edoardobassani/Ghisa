# v216-v217: riquadro «La volta scorsa» all'inizio della seduta con la stessa scheda e promemoria sull'esercizio
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
SET="""async([e,kg,r])=>{const id=S.ex.find(x=>x.name==e).id;S.log.push({id:uid(),d:V.ss.d,e:id,kg,r,ss:V.ss.sid})}"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("""()=>{S.wc=1;xbAdd(['Panca piana bilanciere','Rematore bilanciere','Trazioni']);const I=n=>S.ex.find(x=>x.name==n).id;const t=x=>({s:3,r:8});
      if(S.ex.find(x=>x.name=='Trazioni'))S.ex.find(x=>x.name=='Trazioni').t='bw';
      S.sch.push({id:'sx',name:'Prova',ex:[I('Panca piana bilanciere'),I('Rematore bilanciere'),I('Trazioni')],t:{[I('Panca piana bilanciere')]:t(),[I('Rematore bilanciere')]:t(),[I('Trazioni')]:t()},rt:{}})}""")
    # prima seduta, una settimana fa
    await pg.evaluate("()=>{const d=hvAdd(today(),-7);V.ss={sid:'sA',sc:'sx',fr:0,L:[],i:0,t0:Date.now()-7*864e5-3600e3,d,done:false};V.tab='ss'}")
    for s in [('Panca piana bilanciere',60,8)]*3+[('Rematore bilanciere',50,8)]*3+[('Trazioni',0,8)]*3: await pg.evaluate(SET,list(s))
    await pg.evaluate("()=>{ssEnd();V.ss.t1=V.ss.t0+3600e3;S.ses.find(x=>x.id=='sA').t1=V.ss.t1;V.ss=null}")
    # seconda seduta oggi: panca +2,5, rematore una ripetizione in meno, trazioni uguali
    await pg.evaluate("()=>{V.ss={sid:'sB',sc:'sx',fr:0,L:[],i:0,t0:Date.now()-50*60e3,d:today(),done:false};V.tab='ss'}")
    for s in [('Panca piana bilanciere',62.5,8)]*3+[('Rematore bilanciere',50,8),('Rematore bilanciere',50,8),('Rematore bilanciere',50,7),('Trazioni',0,8),('Trazioni',0,8),('Trazioni',0,8)]: await pg.evaluate(SET,list(s))
    await pg.evaluate("()=>{ssEnd();const o=S.ses.find(x=>x.id=='sB');o.rt='d';o.nt='Spalla un po’ rigida';V.ss=null}")
    await pg.evaluate("()=>{V.ss={sid:'sD',sc:'sx',fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};V.tab='ss';render();scrollTo(0,0)}");await pg.wait_for_timeout(150)
    print('chiuso, una riga:',await pg.evaluate("()=>{const b=$('.lsb');return [b.classList.contains('lsc'),b.querySelector('.lsr span').textContent,Math.round(b.getBoundingClientRect().height),!b.querySelector('.smyt')]}"))
    await pg.screenshot(path=O+'v217-chiuso.png')
    await pg.click('[data-a=lsbt]')
    print('aperto:',await pg.evaluate("()=>{const b=$('.lsb');return [b.querySelector('.hint').textContent,(b.querySelector('.lsq')||{}).textContent,[...b.querySelectorAll('.smyt li')].map(x=>x.textContent)]}"))
    print('subito sotto la barra in alto:',await pg.evaluate("()=>$('.sst').nextElementSibling.classList.contains('lsb')"))
    print('confronto:',await pg.evaluate("()=>[...document.querySelectorAll('.lsb .smyc')].map(c=>c.querySelector('b').textContent+' '+c.querySelector('.smyb').textContent)"))
    h=await pg.evaluate('()=>document.documentElement.scrollHeight');await pg.set_viewport_size({'width':390,'height':h});await pg.screenshot(path=O+'v216-aperto.png');await pg.set_viewport_size({'width':390,'height':844})
    await pg.click('[data-a=lsbt]')
    # promemoria sull'esercizio del rematore
    await pg.evaluate("()=>{V.ss.i=1;render()}");print('promemoria rematore:',await pg.evaluate("()=>($('.lsch')||{}).textContent||'nessuno'"))
    await pg.evaluate("()=>{V.ss.i=0;render()}");print('panca (consiglio «prova» già nella riga Prova):',await pg.evaluate("()=>($('.lsch')||{}).textContent||'nessuno'"))
    # dopo la prima serie il riquadro sparisce
    await pg.evaluate("()=>{S.log.push({id:uid(),d:today(),e:S.ex.find(x=>x.name=='Panca piana bilanciere').id,kg:62.5,r:8,ss:'sD'});render()}")
    print('dopo la prima serie riquadro sparito:',await pg.evaluate("()=>!$('.lsb')"))
    # la × lo chiude per quella seduta
    await pg.evaluate("()=>{S.log=S.log.filter(l=>l.ss!='sD');render()}");await pg.click('[data-a=lsbx]');print('× chiude:',await pg.evaluate("()=>[!$('.lsb'),V.ss.lsx]"))
    # seduta libera e scheda mai fatta: niente riquadro
    await pg.evaluate("()=>{V.ss={sid:'sE',sc:'',fr:1,L:[S.ex[0].id],i:0,t0:Date.now(),d:today(),done:false};render()}");print('seduta libera, nessun riquadro:',await pg.evaluate("()=>!$('.lsb')"))
    await pg.evaluate("()=>{S.sch.push({id:'sy',name:'Nuova',ex:[S.ex[0].id],t:{},rt:{}});V.ss={sid:'sF',sc:'sy',fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};render()}");print('scheda nuova, nessun riquadro:',await pg.evaluate("()=>!$('.lsb')"))
    await pg.evaluate("()=>{V.ss=null;V.tab='h';render()}")
    print('errori',E);await b.close()
asyncio.run(m())
