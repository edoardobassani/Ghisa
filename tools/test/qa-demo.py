import asyncio,re,json
from playwright.async_api import async_playwright
P='file:///home/claude/ghisa/tools/demo/gymbo-demo.html';O='/home/claude/w/qa/'
VIEWS=[('h',"V.tab='h'"),('w',"V.tab='w';V.wv='a'"),('w_st',"V.tab='w';V.wv='h'"),('w_rm',"V.tab='w';V.wv='m'"),('s',"V.tab='s';V.o.dBpw=true"),('s_pg',"V.tab='s';V.pg={f:'bp'}"),('s_prev',"V.tab='s';V.pg=null;V.bpv={k:'ul'}"),('s_ed',"V.tab='s';V.bpv=null;V.bpe={def:bpRes(bpmPB()),dk:0}"),('e',"V.tab='s';V.bpe=null;V.tab='e'"),
 ('c',"V.tab='c';V.cdm='m';V.o.dCd=true"),('c_f',"V.tab='c';V.cdm='f';V.o.dCd=false"),('c_l',"V.tab='c';V.cdm='l'"),('c_pg',"V.tab='c';V.cp={f:'m'}"),('c_prev',"V.tab='c';V.cp={id:'vo2'}"),
 ('n',"V.cp=null;V.tab='n'"),('pp',"V.tab='pp'"),('o',"V.tab='o'"),('g',"V.tab='g';V.o.gr_pal=true;V.o.gr_mm=true"),('g2',"V.tab='g';V.o.gr_pal=false;V.o.gr_mm=false;V.o.gr_cd=true;V.o.gr_pmc=true"),('p',"V.tab='p'"),('x',"V.tab='x'"),('r',"V.tab='r'")]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    E=[];C=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('console',lambda m:C.append(m.text) if m.type=='error' else None)
    await pg.goto(P);await pg.wait_for_timeout(1200)
    for k,js in VIEWS:
      t0=await pg.evaluate("()=>performance.now()")
      try:await pg.evaluate("()=>{"+js+";render();scrollTo(0,0)}")
      except Exception as ex:print('EXC',k,str(ex)[:200]);continue
      ms=await pg.evaluate(f"()=>Math.round(performance.now()-{t0})")
      await pg.wait_for_timeout(300)
      r=await pg.evaluate("""()=>{const t=document.querySelector('#v').innerText;const bad=(t.match(/\\b(undefined|NaN|null|Infinity)\\b|\\[object/g)||[]);
        const wide=[...document.querySelectorAll('#v *')].filter(e=>e.getBoundingClientRect().right>innerWidth+2&&getComputedStyle(e).position!='fixed').slice(0,4).map(e=>e.tagName+'.'+e.className+':'+(e.textContent||'').slice(0,30));
        return {sw:document.documentElement.scrollWidth,bad:[...new Set(bad)],wide}}""")
      flag='' if (r['sw']<=390 and not r['bad'] and not r['wide']) else ' <<<'
      print(k,ms,'ms',r,flag)
      await pg.screenshot(path=O+k+'.png',full_page=True)
    print('ERR',E[:5],'CONSOLE',C[:5]);await b.close()
asyncio.run(main())
