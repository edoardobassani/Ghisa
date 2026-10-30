import asyncio
from playwright.async_api import async_playwright
D=open('/home/claude/w/demo/demo_data.json').read()
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(500)
    ev=lambda j:pg.evaluate(j)
    print(await ev("()=>{const pl0=JSON.stringify(S.pl);bpStart(bpRes(bpm531()),[0,1,3,4]);render();return [S.bp.n,S.bp.sch.length,JSON.stringify(S.pl),pl0]}"))
    print('sett1 military',await ev("()=>{const sc=S.sch.find(x=>x.id==S.bp.sch[0]);const e=sc.ex[0];return [nm(e),S.bp.tm[e],sc.t[e].sets.map(x=>x.r+'@'+x.kg).join(' ')]}"))
    # seduta: AMRAP set via ssa handler
    await ev("()=>{V.ss={sid:'q1',sc:S.bp.sch[0],fr:0,L:[],i:0,t0:Date.now(),d:today(),done:false};V.tab='ss';render()}")
    e=await ev("()=>S.sch.find(x=>x.id==S.bp.sch[0]).ex[0]")
    msg=await ev(f"()=>bpAm('{e}',45,4)");print('amrap ok',msg)
    msg=await ev(f"()=>bpAm('{e}',45,2)");print('amrap ko',msg,await ev("()=>S.bp.amf"))
    # complete 4 weeks
    for w in range(4):
      await ev(f"()=>{{V.ss=null;S.bp.sch.forEach((id,k)=>S.ses.push({{id:'z{w}'+k,d:today(),sc:id,t0:Date.now()+{w}*10,t1:Date.now()+5+{w}*10}}));render()}}")
      await pg.wait_for_timeout(50)
    print('dopo ciclo',await ev(f"()=>[S.bp.wk,S.bp.cyc,S.bp.tm['{e}'],Object.keys(S.bp.amf).length]"))
    # edit active: add week to cycle block
    await ev("()=>{V.tab='s';render()}");await pg.click('[data-a=bped]');await pg.click('[data-a=bpbw][data-i=\"1\"][data-v=\"1\"]');await pg.click('[data-a=bpsv]');print('edit',await ev("()=>[bpW(S.bp),S.bp.B.map(b=>b.w)]"))
    
    await pg.click('[data-a=bpend]');await pg.click('[data-a=bpend]');print('fine',await ev("()=>[S.bp,JSON.stringify(S.pl)]"))
    print('errs',E);await b.close()
asyncio.run(main())
