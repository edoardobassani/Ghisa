# v193: import del piano del nutrizionista in formato Nutrium (pasti con orario, sottosezioni, alternative ○, quantità non in grammi)
import asyncio,subprocess,time,sys,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC)
srv=subprocess.Popen(['python3','-m','http.server','8766','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
O=W+'/u/';os.makedirs(O,exist_ok=True)
async def one(b,f,show):
  pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  await pg.goto('http://127.0.0.1:8766/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
  await pg.evaluate("()=>{S.wc=1;V.tab='pp';render()}");await pg.set_input_files('#ipf','pdft/'+f);await pg.wait_for_timeout(1800)
  st=await pg.evaluate("()=>V.ip?{n:V.ip.rows.length,grp:new Set(V.ip.rows.filter(r=>r.o).map(r=>r.o)).size,days:[...new Set(V.ip.rows.map(r=>r.d))],meals:[...new Set(V.ip.rows.map(r=>r.m))]}:document.querySelector('#toast').textContent")
  print(f,'→',st)
  if show:
    rows=await pg.evaluate("()=>V.ip.rows.map(r=>[r.m.slice(0,8),r.o||'-',r.ga?'alt':'', r.a,r.g,r.cv||'',r.nt||'',(V.ip.map[nrm(r.a).trim()]||{}).st,(fo((V.ip.map[nrm(r.a).trim()]||{}).to)||{}).name||''])")
    for r in rows:print('  ',r)
  await pg.screenshot(path=O+f+'-1.png',full_page=True)
  await pg.evaluate("()=>document.querySelector('[data-a=ipgo][data-s=\"2\"]').click()");await pg.wait_for_timeout(200)
  await pg.screenshot(path=O+f+'-2.png',full_page=True)
  await pg.evaluate("()=>document.querySelector('[data-a=ipgo][data-s=\"3\"]').click()");await pg.wait_for_timeout(200)
  await pg.evaluate("()=>document.querySelector('[data-a=ipok]').click()");await pg.wait_for_timeout(300)
  r=await pg.evaluate("()=>{const W=Object.keys(S.mpw)[0],d=S.mpw[W][0];return [document.querySelector('#toast').textContent,Object.fromEntries(MP.map(m=>[m,d[m].map(x=>fo(x.f).name+' '+x.g+'g'+(x.al?' ['+x.al.length+' scelte: '+x.al.map(a=>fo(a.f).name+' '+a.g).join(' | ')+']':''))])),Object.keys(S.mpw[W]).length]}")
  print('  salvato:',r[0],'giorni',r[2]);
  if show:
    for m,L in r[1].items():
      for x in L:print('    ',m,':',x)
  print('  errori',E);await pg.close()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    await one(b,'nutrium_circ.pdf',True)
    await one(b,'nutrium_o.pdf',False)
    await one(b,'nutrium_gap.pdf',False)
    await one(b,'diet_text.pdf',False)
    await b.close()
asyncio.run(m());srv.terminate()
