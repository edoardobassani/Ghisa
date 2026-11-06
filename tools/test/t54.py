# v215: riepilogo di fine seduta più ricco (confronto, muscoli della settimana, consigli, com'è andata, nota, immagine)
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
    await pg.evaluate("()=>{ssEnd();render();scrollTo(0,0)}");await pg.wait_for_timeout(200)
    print('badge:',await pg.evaluate("()=>[...document.querySelectorAll('.smyc')].map(c=>c.querySelector('b').textContent+' '+c.querySelector('.smyb').textContent)"))
    print('record:',await pg.evaluate("()=>($('.smyr')||{}).textContent||'nessuno'"))
    print('confronto con:',await pg.evaluate("()=>[...document.querySelectorAll('#v .card .hint')].map(x=>x.textContent).find(t=>t.startsWith('Stessa'))"))
    print('consigli:',await pg.evaluate("()=>[...document.querySelectorAll('.smyt li')].map(x=>x.textContent)"))
    print('muscoli:',await pg.evaluate("()=>[...document.querySelectorAll('.smyg')].map(x=>x.innerText.replace(/\\n/g,' '))"))
    print('differenze in alto:',await pg.evaluate("()=>[...document.querySelectorAll('.stat i')].map(x=>x.textContent+' '+x.className)"))
    await pg.click('[data-a=ssrt][data-v=d]');await pg.fill('#ssnt','Spalla un po’ rigida');await pg.press('#ssnt','Tab');await pg.wait_for_timeout(150)
    print('valutazione e nota salvate:',await pg.evaluate("()=>{const o=S.ses.find(x=>x.id=='sB');return [o.rt,o.nt,$('[data-a=ssrt][data-v=d]').classList.contains('on')]}"))
    h=await pg.evaluate('()=>document.documentElement.scrollHeight');await pg.set_viewport_size({'width':390,'height':h});await pg.screenshot(path=O+'v215-riepilogo.png');await pg.set_viewport_size({'width':390,'height':844})
    # indietro e di nuovo fine: valutazione e nota restano
    await pg.click('[data-a=ssp]');await pg.wait_for_timeout(100);await pg.evaluate("()=>{ssEnd();render()}")
    print('dopo Indietro e nuova chiusura:',await pg.evaluate("()=>{const o=S.ses.filter(x=>x.id=='sB');return [o.length,o[0].rt,o[0].nt,$('#ssnt').value]}"))
    # un secondo tocco sulla stessa valutazione la toglie
    await pg.click('[data-a=ssrt][data-v=d]');print('tocco di nuovo su Dura:',await pg.evaluate("()=>S.ses.find(x=>x.id=='sB').rt===undefined"));await pg.click('[data-a=ssrt][data-v=g]')
    # immagine
    sz=await pg.evaluate("async()=>{const b=await ssImg('sB');const bm=await createImageBitmap(b);return [b.type,b.size>5000,bm.width,bm.height]}");print('immagine:',sz)
    await pg.evaluate("async()=>{const b=await ssImg('sB');window.__u=URL.createObjectURL(b)}");p2=await ctx.new_page();await p2.goto(await pg.evaluate("()=>window.__u"));await p2.screenshot(path=O+'v215-img.png',full_page=True);await p2.close()
    # seduta libera senza scheda: niente errore, confronto con l'ultima volta di ogni esercizio
    await pg.evaluate("()=>{V.ss={sid:'sC',sc:'',fr:1,L:[S.ex.find(x=>x.name=='Panca piana bilanciere').id],i:0,t0:Date.now()-20*60e3,d:today(),done:false};V.tab='ss'}")
    await pg.evaluate(SET,['Panca piana bilanciere',65,5]);await pg.evaluate("()=>{ssEnd();render()}")
    print('seduta libera:',await pg.evaluate("()=>[$('#v h1').textContent,[...document.querySelectorAll('#v .card .hint')].map(x=>x.textContent).find(t=>t.startsWith('L’ultima')),$('.smyb').textContent]"))
    # a fine seduta la Home funziona
    await pg.click('[data-a=ssx]');await pg.wait_for_timeout(150);print('Fine porta fuori:',await pg.evaluate("()=>V.tab"))
    print('errori',E);await b.close()
asyncio.run(m())
