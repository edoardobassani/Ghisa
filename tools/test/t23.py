import asyncio,json
from playwright.async_api import async_playwright
from t import SEED
D='/home/claude/w/gxs/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400)
    await pg.evaluate(SEED);await pg.evaluate("()=>{S.pf=S.pf||{};S.pf.age=35;S.pf.sx='m';S.cd.push({id:'c1',d:'2026-10-25',t:'Bici',min:40,km:15});save()}");await pg.reload();await pg.wait_for_timeout(500)
    await pg.evaluate("()=>{V.tab='c';render()}")
    await pg.screenshot(path='/home/claude/w/out3/0-cardio.png')
    await pg.set_input_files('#gxf',[D+f for f in ['strava.gpx','huawei.gpx','komoot.gpx','garmin.tcx','track.kml','export.zip','broken.gpx']])
    await pg.wait_for_timeout(1200)
    r=await pg.evaluate("()=>V.gi&&{err:V.gi.err,L:V.gi.L.map(a=>({f:a.file,d:a.d,ty:a.ty,sel:a.sel,src:a.src,mv:a.mv,el:a.el,km:a.km,asc:a.asc,hr:a.hr,fkc:a.fkc,noT:a.noT,sp:a.sp.length,rt:a.rt.split(';').length,dup:a.dup,kc:gxKc(a)}))}")
    print(json.dumps(r,indent=0))
    for i in range(len(r['L'])):
      await pg.evaluate(f"()=>{{V.gi.i={i};render();scrollTo(0,0)}}");await pg.wait_for_timeout(150)
      await pg.screenshot(path=f'/home/claude/w/out3/p{i}.png',full_page=True)
    # komoot: give minutes
    ki=[x['f'] for x in r['L']].index('komoot.gpx')
    await pg.evaluate(f"()=>{{V.gi.i={ki};render()}}");await pg.fill('#gim','55');
    hb=[x['f'] for x in r['L']].index('huawei.gpx')
    await pg.evaluate(f"()=>{{V.gi.i={hb};render()}}");await pg.click('[data-a=gidp][data-v=rep]')
    await pg.click('[data-a=gisave]');await pg.wait_for_timeout(300)
    print(await pg.evaluate("()=>({n:S.cd.length,c1:!!S.cd.find(c=>c.id=='c1'),L:S.cd.map(c=>[c.d,c.t,c.min,c.km,c.kc,c.est||0,c.from||'',c.asc,c.hr&&c.hr.a,(c.sp||[]).length])})"))
    await pg.evaluate("()=>{V.o.dCd=true;const c=S.cd.find(c=>c.from=='Strava');V.o['gxc_'+c.id]=true;render()}")
    await pg.wait_for_timeout(200)
    el=await pg.query_selector('#dCd');await el.screenshot(path='/home/claude/w/out3/h.png')
    # reimport same -> all duplicates
    await pg.set_input_files('#gxf',[D+'strava.gpx']);await pg.wait_for_timeout(800)
    print('reimport',await pg.evaluate("()=>V.gi&&V.gi.L.map(a=>a.dup)"))
    await pg.screenshot(path='/home/claude/w/out3/dup.png')
    # undo test
    await pg.click('[data-a=gix]');
    print('errs',errs);await b.close()
asyncio.run(main())
