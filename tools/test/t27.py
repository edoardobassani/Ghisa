import asyncio,json
from playwright.async_api import async_playwright
D=open('/home/claude/w/demo/demo_data.json').read()
O='/home/claude/w/out6/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(500)
    ev=lambda js:pg.evaluate(js)
    async def shot(n,full=True):
      await pg.wait_for_timeout(250);await pg.evaluate("()=>document.activeElement&&document.activeElement.blur()");await pg.screenshot(path=O+n,full_page=full)
    # Massimali
    await ev("()=>{V.tab='w';V.wv='m';render()}");await shot('1-massimali.png')
    print('rm',await ev("()=>['Squat','Panca piana bilanciere','Stacco da terra'].map(n=>{const e=S.ex.find(x=>x.name==n);return e?[n,rmOf(e.id),tmOf(e.id)]:[n,null]})"))
    sq=await ev("()=>S.ex.find(x=>x.name=='Stacco da terra').id")
    await pg.click(f'[data-a=rme][data-i="{sq}"]');await pg.wait_for_timeout(200);await shot('2-edit.png',False)
    await pg.fill('#rmkg','175');await pg.check('#rmt');await pg.click('[data-a=rms]');await pg.wait_for_timeout(200)
    print('stacco',await ev(f"()=>[rmOf('{sq}'),tmOf('{sq}')]"))
    # programmi pronti -> 5/3/1
    await ev("()=>{V.tab='s';V.pg={};render()}");await pg.click('[data-a=pgf][data-k=bp]');await pg.wait_for_timeout(200);await shot('3-pronti.png',False)
    await pg.click('[data-a=bpvo][data-k=lin]');await pg.wait_for_timeout(200);await shot('4-prev.png')
    await pg.click('[data-a=bpgo]');await pg.wait_for_timeout(200)
    for d in ['0','2','4']:await pg.click(f'[data-a=bpday][data-i="{d}"]')
    await shot('5-avvia.png',False)
    await pg.click('[data-a=bpgo2]');await pg.wait_for_timeout(300);await ev("()=>{V.o.dBpw=true;render();scrollTo(0,0)}");await shot('6-schede.png')
    print('bp',await ev("()=>({n:S.bp.n,wk:S.bp.wk,sch:S.bp.sch.length,pl:S.pl,tm:Object.fromEntries(Object.entries(S.bp.tm).map(([k,v])=>[nm(k),v]))})"))
    print('scA',await ev("()=>{const sc=S.sch.find(x=>x.id==S.bp.sch[0]);return [sc.name,sc.ex.map(e=>nm(e)+': '+JSON.stringify(sc.t[e].sets))]}"))
    # Home
    await ev("()=>{V.tab='h';render();scrollTo(0,0)}");await shot('7-home.png',False)
    # seduta giorno A
    await ev("()=>{V.ss={sid:'ssA',sc:S.bp.sch[0],fr:0,L:[],i:0,t0:Date.now()-3600e3,d:today(),done:false};V.tab='ss';render();scrollTo(0,0)}");await shot('8-seduta.png')
    # finish all 3 days -> week advances
    await ev("()=>{S.bp.sch.forEach((id,k)=>{S.ses.push({id:'sx'+k,d:today(),sc:id,t0:Date.now(),t1:Date.now()+1000,n:5})});V.ss=null;V.tab='s';render()}")
    print('dopo sett.',await ev("()=>[S.bp.wk,S.sch.find(x=>x.id==S.bp.sch[0]).t[S.bp.D[0].it[0].e].sets.map(x=>x.r+'@'+x.kg).join(',')]"))
    # costruttore
    await ev("()=>{V.tab='s';render()}");await pg.click('[data-a=bpnew]');await pg.wait_for_timeout(200)
    sid=await ev("()=>S.ex.find(x=>x.name=='Squat').id")
    await pg.select_option('#bpadd',sid);await pg.wait_for_timeout(200)
    await pg.click('[data-a=bpty][data-v=t]');await pg.wait_for_timeout(150);await pg.click('[data-a=bpty][data-v=p]');await pg.wait_for_timeout(150)
    await pg.click('.bpqf summary');await pg.fill('#bqs_0','5');await pg.fill('#bqr_0','5');await pg.fill('#bqv_0','72.5');await pg.fill('#bqd_0','2.5');await pg.click('[data-a=bpqf]');await pg.wait_for_timeout(200)
    await pg.fill('.bpf[data-w="0"][data-k="r"]','6');await pg.click('h2');await pg.wait_for_timeout(200)
    await pg.click('[data-a=bpbw][data-i="0"][data-v="1"]');await pg.wait_for_timeout(150)
    await pg.click('[data-a=bpda]');await pg.wait_for_timeout(150);await pg.click('[data-a=bpdk][data-i="0"]');await pg.wait_for_timeout(150)
    await shot('9-costruttore.png')
    print('draft',await ev("()=>{const d=V.bpe.def;return {B:d.B.map(b=>b.n+b.w),W:d.D[0].it[0].W.map(bpTxt)}}"))
    await pg.click('[data-a=bpsl]');print('lib',await ev("()=>S.bpl.map(x=>x.n)"))
    print('errs',E);await b.close()
asyncio.run(main())
