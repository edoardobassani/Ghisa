# v263: schede semplici «a tabella»
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl={};save()}",D);await pg.reload();await pg.wait_for_timeout(800)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    sid=await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.remove();const s=S.sch.find(s=>!bpOwn(s)&&s.ex.length>=4)||S.sch[0];V.tab='s';V.ed=s.id;V.sd=null;render();return s.id}");await pg.wait_for_timeout(300)
    n=await pg.evaluate("()=>V.sd.ex.length")
    ok(await pg.locator('table.sdt').count()==1 and await pg.locator('table.sdt tbody tr').count()==n,f'si apre in Tabella con {n} righe')
    await pg.screenshot(path=gb.O+'/t98a.png',full_page=True)
    async def ctr(r):
      await pg.evaluate(f"()=>document.querySelector('.sdt td[data-r=\"{r}\"]').scrollIntoView({{block:'center'}})");await pg.wait_for_timeout(80)
    async def tap(r):
      await ctr(r);bb=await pg.locator(f'.sdt td[data-r="{r}"]').first.bounding_box();await pg.mouse.move(bb['x']+10,bb['y']+10);await pg.mouse.down();await pg.wait_for_timeout(50);await pg.mouse.up();await pg.wait_for_timeout(150)
    await tap(0)
    ok(await pg.locator('.sdtf[data-k=s]').count()==1,'tocco: barra con serie, ripetizioni, carico, recupero')
    await pg.fill('.sdtf[data-k=s]','5');await pg.fill('.sdtf[data-k=r]','5');await pg.fill('.sdtf[data-k=kg]','80');await pg.fill('.sdtf[data-k=rc]','180');await pg.wait_for_timeout(100)
    r=await pg.evaluate("()=>{const i=V.sd.ex[0];return [V.sd.t[i].s,V.sd.t[i].r,V.sd.t[i].kg,V.sd.rt[i],document.querySelector('.sdt tbody tr').innerText.replace(/\\s+/g,' ')]}");print(r)
    ok(r[:4]==[5,5,80,180],'valori scritti nella scheda e tabella aggiornata')
    await pg.screenshot(path=gb.O+'/t98b.png')
    # più righe: pressione lunga e trascinamento in verticale
    await ctr(1);b1=await pg.locator('.sdt td[data-r="1"]').first.bounding_box()
    await pg.mouse.move(b1['x']+10,b1['y']+10);await pg.mouse.down();await pg.wait_for_timeout(520)
    for k in (2,3):
      bb=await pg.locator(f'.sdt td[data-r="{k}"]').first.bounding_box();await pg.mouse.move(bb['x']+10,bb['y']+10,steps=3);await pg.wait_for_timeout(60)
    await pg.mouse.up();await pg.wait_for_timeout(200)
    s=await pg.evaluate("()=>V.sd.tsel");ok(s=={'a':1,'b':3},'3 righe selezionate '+str(s))
    await pg.fill('#sdt_s','4');await pg.fill('#sdt_rc','90');await pg.click('[data-a=sdtap]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>V.sd.ex.slice(1,4).map(i=>isCX(i)?['cx',V.sd.rt[i]]:[V.sd.t[i]&&V.sd.t[i].s,V.sd.rt[i]])");print(r)
    ok(all(x[1]==90 for x in r) and all(x[0] in (4,'cx') for x in r),'serie e recupero applicati a 3 esercizi')
    await pg.screenshot(path=gb.O+'/t98c.png')
    # copia e incolla
    await tap(0);await pg.click('[data-a=sdtcp]');await tap(4);await pg.click('[data-a=sdtpa]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>{const a=V.sd.ex[0],b=V.sd.ex[4];return isCX(b)?'cx':[V.sd.t[b].s,V.sd.t[b].r,V.sd.rt[b]]}");ok(r=='cx' or r==[5,5,180],'riga incollata '+str(r))
    # superserie dal nome
    await pg.click('.sdt tbody tr:nth-child(2) td.ex button');await pg.wait_for_timeout(150)
    await pg.click('#bptsh [data-a=sdln]');await pg.wait_for_timeout(150)
    ok(await pg.locator('.sdt tr.sdts').count()>=2,'superserie creata dal nome e segnata in tabella')
    await pg.screenshot(path=gb.O+'/t98d.png')
    await pg.click('#bptsh [data-a=sdtshx]')
    # annulla
    await pg.click('[data-a=sdtu]');await pg.wait_for_timeout(150);ok(await pg.locator('.sdt tr.sdts').count()==0,'«Annulla» toglie la superserie')
    # piramide → misto
    r=await pg.evaluate("()=>{const i=V.sd.ex[0];V.sd.t[i]={s:3,r:10,sets:[{r:10,kg:60},{r:8,kg:70},{r:6,kg:80}]};V.sd.tsel={a:0,b:0};render();return document.querySelector('.sdt tbody tr').innerText.includes('serie diverse')}");ok(r,'piramide mostrata come «serie diverse»')
    await pg.click('[data-a=sdtsimp]');await pg.wait_for_timeout(100)
    r=await pg.evaluate("()=>{const t=V.sd.t[V.sd.ex[0]];return [t.s,t.r,t.kg]}");ok(r==[3,6,80],'«Rendile uguali» usa l’ultima serie '+str(r))
    # Dettaglio
    await pg.click('[data-a=sdtv][data-v=d]');await pg.wait_for_timeout(150);ok(await pg.locator('.sdlst').count()==1,'«Dettaglio» = editor di prima')
    await pg.click('[data-a=sdtv][data-v=t]');await pg.wait_for_timeout(150)
    # salva
    await pg.click('[data-a=sca]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("(id)=>{const s=S.sch.find(x=>x.id==id),i=s.ex[0];return [s.t[i].s,s.t[i].kg,s.rt[i],V.sd]}",sid);ok(r[:3]==[3,80,180],'scheda salvata '+str(r[:3]))
    # nuova scheda: esercizi dal selettore
    await pg.evaluate("()=>{V.ed='';V.sd=null;render()}");await pg.wait_for_timeout(150)
    await pg.click('[data-a=sdpk]');await pg.wait_for_timeout(200);await pg.locator('#sdl .sdi input:not([disabled])').nth(0).check();await pg.locator('#sdl .sdi input:not([disabled])').nth(1).check()
    await pg.click('[data-a=sdpa]') if await pg.locator('[data-a=sdpa]').count() else None;await pg.wait_for_timeout(200)
    print('nuova',await pg.evaluate("()=>V.sd.ex.length"))
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
