import asyncio,subprocess,json,time
from playwright.async_api import async_playwright
srv=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/w',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('console',lambda c:E.append('C:'+c.text) if c.type=='error' else None)
    await pg.goto('http://127.0.0.1:8765/tracker-palestra.html');await pg.wait_for_timeout(800)
    async def sheets(f):
      return await pg.evaluate("""async f=>{const r=await fetch('pdft/'+f);const b=await r.arrayBuffer();try{const s=await pdfSheets(b);return {g:s[0].g,lines:s[0].lines}}catch(e){return {err:e.message}}}""",f)
    # gym table
    s=await sheets('gym_table.pdf');print('GRID gym_table:');[print('  ',r) for r in s['g'][:14]]
    r=await pg.evaluate("""async()=>{const b=await (await fetch('pdft/gym_table.pdf')).arrayBuffer();const sh=imPrep(await pdfSheets(b));return imBlocks(sh[0].g).map(x=>({day:x.day,rows:x.rows.map(r=>[r.n,r.s,r.rep,r.rec,r.nt].join('|'))}))}""");print('BLOCKS gym_table',json.dumps(r,ensure_ascii=False,indent=0))
    r=await pg.evaluate("""async()=>{const b=await (await fetch('pdft/gym_text.pdf')).arrayBuffer();const sh=imPrep(await pdfSheets(b));return imBlocks(sh[0].g).map(x=>({day:x.day,rows:x.rows.map(r=>[r.n,r.s,r.rep,r.kg,r.rec,r.nt].join('|'))}))}""");print('BLOCKS gym_text',json.dumps(r,ensure_ascii=False,indent=0))
    for f in ['diet_text.pdf','diet_table.pdf']:
      r=await pg.evaluate("""async f=>{const b=await (await fetch('pdft/'+f)).arrayBuffer();const sh=ipPrep(await pdfSheets(b));return sh.flatMap(s=>ipRows(s.g).rows).map(r=>[r.d,r.m,r.a,r.g,r.alt?'ALT':''].join('|'))}""",f);print('DIET',f);[print('  ',x) for x in r]
    for f in ['cardio_text.pdf','cardio_table.pdf']:
      r=await pg.evaluate("""async f=>{const b=await (await fetch('pdft/'+f)).arrayBuffer();const sh=await pdfSheets(b);ccLoad(sh,f);return V.ci.L.map(x=>x.n+' | '+x.t+' | di='+x.di+' | '+(x.B.length?cpTxt(cbSpec(x.B)):'VUOTO')+' | bad='+x.bad.join(';'))}""",f);print('CARDIO',f);[print('  ',x) for x in r]
    r=await sheets('scan.pdf');print('SCAN',r.get('err'))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
