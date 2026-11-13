# v262: editor dei programmi «a tabella»
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=False);pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.agl={};save()}",D);await pg.reload();await pg.wait_for_timeout(800)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    await pg.evaluate("()=>{const e=document.querySelector('#agun');if(e)e.remove();V.tab='s';render()}");await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{const p=S.bp;V.bpe={def:JSON.parse(JSON.stringify({n:p.n,rep:p.rep,B:p.B,D:p.D})),dk:0,act:1};render()}");await pg.wait_for_timeout(300)
    W=await pg.evaluate("()=>bpW(V.bpe.def)");nx=await pg.evaluate("()=>V.bpe.def.D[0].it.length")
    ok(await pg.locator('table.bpt').count()==1,'si apre in Tabella')
    ok(await pg.locator('table.bpt tbody tr').count()==nx and await pg.locator('table.bpt tbody tr:first-child td[data-w]').count()==W,f'{nx} righe × {W} settimane')
    ok(await pg.locator('table.bpt tr.bk th button').count()==await pg.evaluate("()=>V.bpe.def.B.length"),'intestazioni dei blocchi')
    await pg.screenshot(path=gb.O+'/t97a.png',full_page=True)
    async def ctr(x,w):
      await pg.evaluate(f"()=>document.getElementById('bc_{x}_{w}').scrollIntoView({{block:'center'}})");await pg.wait_for_timeout(80)
    async def tap(x,w):
      await ctr(x,w);bb=await pg.locator(f'#bc_{x}_{w}').bounding_box();await pg.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2);await pg.mouse.down();await pg.wait_for_timeout(60);await pg.mouse.up();await pg.wait_for_timeout(150)
    await tap(0,2)
    ok(await pg.locator('#bc_0_2.sel').count()==1 and await pg.locator('.bptf').count()>=3,'tocco: cella scelta e barra in basso')
    await pg.fill('.bptf[data-k=s]','6');await pg.wait_for_timeout(100)
    c=await pg.inner_text('#bc_0_2');ok(c.startswith('6×'),'la cella cambia mentre scrivi: '+c.replace('\n',' '))
    await pg.screenshot(path=gb.O+'/t97b.png')
    # pressione lunga e trascinamento da S1 a S4 dell'esercizio 2 (Panca)
    await ctr(1,0);b0=await pg.locator('#bc_1_0').bounding_box();b3=await pg.locator('#bc_1_3').bounding_box()
    await pg.mouse.move(b0['x']+20,b0['y']+20);await pg.mouse.down();await pg.wait_for_timeout(550)
    for k in range(1,4):
      bb=await pg.locator(f'#bc_1_{k}').bounding_box();await pg.mouse.move(bb['x']+20,bb['y']+20,steps=3);await pg.wait_for_timeout(60)
    await pg.mouse.up();await pg.wait_for_timeout(200)
    s=await pg.evaluate("()=>V.bpe.sel");ok(s=={'x':1,'w0':0,'w1':3},'trascinamento: 4 settimane selezionate '+str(s))
    await pg.click('[data-a=bptfill]');await pg.wait_for_timeout(150)
    await pg.click('[data-a=bptfm][data-v=p]');await pg.wait_for_timeout(150)
    await pg.fill('#bpts_v','5');await pg.wait_for_timeout(100)
    pv=await pg.inner_text('.bptpv');print(pv.replace('\n',' '))
    await pg.screenshot(path=gb.O+'/t97c.png')
    await pg.click('[data-a=bptfa]');await pg.wait_for_timeout(200)
    v=await pg.evaluate("()=>V.bpe.def.D[0].it[1].W.slice(0,4).map(L=>[L.length,L[0].r,L[0].p])");print(v)
    ok([x[2] for x in v]==[v[0][2]+5*k for k in range(4)] and len(set((x[0],x[1]) for x in v))==1,'progressione +5% a settimana applicata')
    # copia e incolla su un'altra riga
    await pg.click('[data-a=bptcp]');await tap(2,0);await pg.click('[data-a=bptpa]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>{const d=V.bpe.def.D[0];return [d.it[1].ty,d.it[2].ty,V.bpe.sel]}");print('incolla',r)
    # riempi → fino a fine blocco
    await tap(0,0);await pg.click('[data-a=bptfr]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>{const it=V.bpe.def.D[0].it[0],b=V.bpe.def.B[0].w;return it.W.slice(0,b).every(L=>JSON.stringify(L)==JSON.stringify(it.W[0]))}");ok(r,'«Riempi →» copia fino alla fine del blocco')
    # blocco: una settimana in più e duplica
    w0=await pg.evaluate("()=>bpW(V.bpe.def)")
    await pg.click('table.bpt tr.bk th:nth-child(2) button');await pg.wait_for_timeout(150)
    await pg.click('#bptsh [data-a=bptbw][data-v="1"]');await pg.wait_for_timeout(150)
    await pg.click('#bptsh [data-a=bptbd]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>[bpW(V.bpe.def),V.bpe.def.B.map(b=>b.n+':'+b.w).join(','),V.bpe.def.D.every(d=>d.it.every(it=>it.W.length==bpW(V.bpe.def)))]");print(r)
    ok(r[0]==w0+1+(await pg.evaluate("()=>V.bpe.def.B[0].w")) and r[2],'settimana in più e blocco duplicato, colonne coerenti in tutti i giorni')
    await pg.screenshot(path=gb.O+'/t97d.png')
    await pg.click('#bptsh [data-a=bptshx]')
    # annulla due volte
    await pg.click('[data-a=bptu]');await pg.click('[data-a=bptu]');await pg.wait_for_timeout(150)
    ok(await pg.evaluate("()=>bpW(V.bpe.def)")==w0,'«Annulla» torna indietro')
    # esercizio: tipo
    await pg.click('table.bpt tbody tr:nth-child(3) td.ex button');await pg.wait_for_timeout(150)
    await pg.click('#bptsh [data-a=bpty][data-v=k]');await pg.wait_for_timeout(150)
    ok(await pg.evaluate("()=>V.bpe.def.D[0].it[2].ty")=='k','tipo di carico cambiato dal nome dell’esercizio')
    await pg.click('#bptsh [data-a=bptshx]')
    # vista Dettaglio
    await pg.click('[data-a=bptv][data-v=d]');await pg.wait_for_timeout(150);ok(await pg.locator('.bpgrid').count()>0,'«Dettaglio» = editor di prima')
    await pg.click('[data-a=bptv][data-v=t]');await pg.wait_for_timeout(150)
    # salva
    await pg.click('[data-a=bpsv]');await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[S.bp.D[0].it[1].W.slice(0,4).map(L=>L[0].p),V.bpe]");ok(r[1] is None and r[0]==[x[2] for x in v],'salvato nel programma attivo')
    # nuovo programma vuoto
    await pg.evaluate("()=>{V.bpe={def:bpNewDef(),dk:0};render()}");await pg.wait_for_timeout(150)
    await pg.select_option('#bpadd',index=2);await pg.wait_for_timeout(200)
    ok(await pg.locator('table.bpt tbody tr').count()==1,'programma nuovo: esercizio aggiunto alla tabella')
    ok(not E,'nessun errore JS '+str(E)[:300]);await b.close()
asyncio.run(m())
