import asyncio,sys,json
from playwright.async_api import async_playwright
SEED=r"""()=>{localStorage.clear();
 xbAdd(['Panca piana bilanciere','Croci con manubri','Lat machine','Rematore manubrio','Curl manubri','Squat','Leg extension','Dip','Piegamenti','Alzate laterali','Military press','Push down corda']);
 S.ex.push({id:'myx',name:'Esercizio mio',g:'Petto'});
 const id=n=>S.ex.find(e=>e.name==n).id;
 const P=['Panca piana bilanciere','Croci con manubri','Lat machine','Rematore manubrio','Curl manubri','Piegamenti'];
 S.sch.push({id:'sA',name:'Push-Pull A',ex:P.map(id),t:{},rt:{},ss:[]});
 const kg={'Panca piana bilanciere':70,'Croci con manubri':16,'Lat machine':55,'Rematore manubrio':26,'Curl manubri':14,'Piegamenti':0};
 for(let w=1;w<=4;w++){const d=dShift(today(),-w*3),ss='old'+w;P.forEach(n=>{for(let s=0;s<3;s++)S.log.push({id:uid(),d,e:id(n),kg:kg[n],r:8,ss})})}
 S.ses=[1,2,3,4].map(w=>({id:'old'+w,d:dShift(today(),-w*3),sc:'sA'}));
 save();}"""
async def run(js_steps,shots=()):
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file://'+__import__('os').environ.get('SRC','/home/claude/w/tracker-palestra.html'));await pg.wait_for_timeout(400)
    await pg.evaluate(SEED);await pg.reload();await pg.wait_for_timeout(500)
    out=[]
    for st in js_steps:
      if isinstance(st,tuple):
        await pg.wait_for_timeout(250);await pg.evaluate("()=>document.activeElement&&document.activeElement.blur()");await pg.screenshot(path=st[0]);continue
      if st.startswith('click:'):
        await pg.click(st[6:]);await pg.wait_for_timeout(150);continue
      try: r=await pg.evaluate(st)
      except Exception as ex: r='EXC '+str(ex).split('\n')[0][:160]+' @ '+st[:70]
      await pg.wait_for_timeout(120)
      if r is not None: out.append(r)
    await b.close();return out,errs
