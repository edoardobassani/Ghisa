# v218: 4 piani pronti «Allenamento e riposo» (2 onnivori, vegetariano, vegano) con più calorie nei giorni di allenamento
import gb
import asyncio,subprocess,time,os,json
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
FIX=gb.T+'/fix/dpm-v217.json'  # i 9 piani di prima, presi dalla v217 (rigenerare solo se cambiano apposta)
SET="()=>{S.wc=1;S.h=180;S.pf={sx:'m',age:35,act:'1.55'};S.wt=[{id:'w1',d:today(),kg:80}];save()}"
OLD="()=>JSON.stringify(DPM.filter(p=>!p[9]).map(p=>{const W=dpWeek(p,'v',dpTarget('m'));return [p[0],W.W.map(L=>L.map(x=>x.f.name+':'+x.g).join(','))]}))"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844});pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    old=open(FIX).read()
    await pg.goto(gb.URL);await pg.wait_for_timeout(800);await pg.evaluate(SET);new=await pg.evaluate(OLD)
    print('i 9 piani di prima sono identici:',old==new,len(json.loads(new)))
    print('alimenti dei piani nuovi tutti in banca dati:',await pg.evaluate("()=>{const M=[];DPM.filter(p=>p[9]).forEach(p=>[p[5],p[6],p[7],p[8],p[9].st].flat().forEach(m=>dpIt(m).forEach(x=>{if(!dpFood(x.n))M.push(x.n)})));return M.length?M:'sì'}"))
    await pg.evaluate("()=>{V.tab='pp';render()}");await pg.click('[data-a=dpl]')
    print('piani nell’elenco:',await pg.evaluate("()=>document.querySelectorAll('.pgc').length"),await pg.evaluate("()=>[...document.querySelectorAll('.pgc b')].map(x=>x.textContent).filter(t=>t.startsWith('Allenamento'))"))
    for k in ['cym','cyp','cyv','cyn']:
      await pg.click(f'[data-a=dpo][data-k={k}]');await pg.wait_for_timeout(100)
      r=await pg.evaluate("()=>{const G=V.dp,p=DPM.find(x=>x[0]==G.id),tg=dpTarget(G.obj),W=dpWeek(p,'v',tg,G.td),k=W.W.map(L=>Math.round(dpTot(L).k));return {td:G.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' '),obj:G.obj,K:tg.K,cy:W.cy,kcal:k,media:Math.round(W.av.k),prot:W.W.map(L=>Math.round(dpTot(L).p)),sp:W.W.map(L=>L.filter(x=>x.m=='Spuntino').map(x=>x.f.name).join('+'))}}")
      print(k,json.dumps(r,ensure_ascii=False))
      await pg.click('[data-a=dpb]')
    await pg.click('[data-a=dpo][data-k=cym]')
    await pg.screenshot(path=O+'v218-dettaglio.png',full_page=True)
    await pg.click('[data-a=dptn][data-v="1"]');print('+1 giorno:',await pg.evaluate("()=>V.dp.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' ')"),await pg.evaluate("()=>$('.dpcn b').textContent"))
    await pg.click('[data-a=dptd][data-v="5"]');print('tocco Sab:',await pg.evaluate("()=>V.dp.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' ')"),await pg.evaluate("()=>$('.dpcn b').textContent"))
    await pg.click('[data-a=dpd][data-v="5"]');print('anteprima sabato:',await pg.evaluate("()=>[...document.querySelectorAll('.hint')].map(x=>x.textContent).find(t=>t.startsWith('Sabato'))"))
    await pg.click('[data-a=dpd][data-v="6"]');print('anteprima domenica:',await pg.evaluate("()=>[...document.querySelectorAll('.hint')].map(x=>x.textContent).find(t=>t.startsWith('Domenica'))"))
    for i in [0,1,2,3,4,5]:
      on=await pg.evaluate(f"()=>V.dp.td[{i}]")
      if on: await pg.click(f'[data-a=dptd][data-v="{i}"]')
    print('non si scende sotto 1 giorno:',await pg.evaluate("()=>V.dp.td.filter(Boolean).length"))
    await pg.click('[data-a=dptn][data-v="1"]');await pg.click('[data-a=dptn][data-v="1"]')
    await pg.click('[data-a=dpu]');await pg.click('[data-a=dpok]');await pg.wait_for_timeout(150)
    r=await pg.evaluate("()=>{const A=S.dpa,w=S.mpw[A.w],k=[0,1,2,3,4,5,6].map(d=>Math.round(MP.reduce((t,m)=>t+(w[d][m]||[]).reduce((u,x)=>u+ln(x).k,0),0)));return {td:A.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' '),goal:S.goal,k}}")
    print('applicato:',json.dumps(r,ensure_ascii=False))
    print('riquadro del piano:',await pg.evaluate("()=>{V.tab='pp';V.dp=null;render();return ($('[data-a=dprc]')||{}).closest?$('[data-a=dprc]').closest('.card').innerText.replace(/\\n/g,' '):''}"))
    await pg.evaluate("()=>{S.wt.push({id:'w2',d:today(),kg:85});}");await pg.click('[data-a=dprc]')
    print('ricalcola tiene i giorni:',await pg.evaluate("()=>S.dpa.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' ')"))
    # giorni presi dal programma settimanale della palestra
    await pg.evaluate("()=>{S.sch.push({id:'sq',name:'A',ex:[],t:{},rt:{}});S.pl={0:'sq',1:'sq',3:'sq',5:'sq'};V.tab='pp';V.dp={id:null,f:''};render()}")
    await pg.click('[data-a=dpo][data-k=cyn]');print('dal programma della palestra:',await pg.evaluate("()=>V.dp.td.map((x,i)=>x?DN[i]:'').filter(Boolean).join(' ')"))
    await pg.screenshot(path=O+'v218-vegano.png',full_page=True)
    print('errori',E);await b.close()
asyncio.run(m())
