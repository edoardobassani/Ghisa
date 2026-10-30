import asyncio,json,time,math,datetime as dt
from playwright.async_api import async_playwright
from t import SEED
O='/home/claude/w/out4/'
MOCK="""(()=>{const L=[];let ch;window.__bt={emit(b){const v=new DataView(new Uint8Array([0,b]).buffer);ch&&ch.l.forEach(f=>f({target:{value:v}}))},drop(){dev.l.forEach(f=>f())}};
const dev={name:'HUAWEI WATCH GT 5-A1B',l:[],addEventListener(e,f){this.l.push(f)},gatt:{connected:false,async connect(){this.connected=true;return{async getPrimaryService(){return{async getCharacteristic(){ch={l:[],addEventListener(e,f){this.l.push(f)},async startNotifications(){}};return ch}}}}},disconnect(){}}};
Object.defineProperty(navigator,'bluetooth',{value:{async requestDevice(){return dev}}});
setInterval(()=>window.__bt.emit(150+Math.round(Math.random()*6)),300)})()"""
async def main():
  # GPX sovrapposto al cardio dal vivo
  now=time.time();t0=now-28*60
  pts=''.join(f'<trkpt lat="{45.46+0.007*math.sin(i/50*math.pi):.6f}" lon="{9.19+0.01*math.cos(i/50*math.pi):.6f}"><ele>{120+5*math.sin(i/10):.1f}</ele><time>{dt.datetime.utcfromtimestamp(t0+i*16.8).strftime("%Y-%m-%dT%H:%M:%SZ")}</time></trkpt>' for i in range(101))
  open('/home/claude/w/gxs/live.gpx','w').write(f'<?xml version="1.0"?><gpx version="1.1" creator="Huawei Health" xmlns="http://www.topografix.com/GPX/1/1"><trk><type>running</type><trkseg>{pts}</trkseg></trk></gpx>')
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(MOCK)
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400)
    await pg.evaluate(SEED);await pg.evaluate("()=>{S.pf=S.pf||{};S.pf.age=35;S.pf.sx='m';save()}");await pg.reload();await pg.wait_for_timeout(500)
    await pg.evaluate("()=>{V.tab='c';render()}");await pg.wait_for_timeout(200)
    el=await pg.query_selector('[data-a=hrc]');await (await el.evaluate_handle("e=>e.closest('.card')")).as_element().screenshot(path=O+'1-off.png')
    await pg.click('[data-a=hrc]');await pg.wait_for_timeout(800)
    print('stato',await pg.evaluate("()=>[HR.st,HR.nm,HR.bpm]"))
    el=await pg.query_selector('[data-a=lcgo]');await (await el.evaluate_handle("e=>e.closest('.card')")).as_element().screenshot(path=O+'2-on.png')
    # 28 minuti di battito nel buffer
    await pg.evaluate("""()=>{const t0=Date.now()-28*60e3;HRB=HRB.filter(x=>x[0]<t0);for(let i=0;i<28*60;i++){const p=i/60;HRB.push([t0+i*1000,Math.round(95+60*Math.min(1,p/5)+(p>18&&p<23?12:0)+Math.sin(i/7)*3)])}HRB.sort((a,b)=>a[0]-b[0])}""")
    await pg.select_option('#lct0','Corsa');await pg.click('[data-a=lcgo]')
    await pg.evaluate("()=>{V.lc.t0=Date.now()-28*60e3;lcKeep();lcUpd.t=0;render()}");await pg.wait_for_timeout(1500)
    await pg.screenshot(path=O+'3-live.png')
    await pg.click('[data-a=lcp]');await pg.wait_for_timeout(300);print('pausa',await pg.evaluate("()=>!!V.lc.pa"));await pg.click('[data-a=lcp]')
    # reload: la registrazione riprende
    await pg.reload();await pg.wait_for_timeout(600);print('dopo reload',await pg.evaluate("()=>V.lc&&[V.lc.t,Math.round(lcEl(V.lc)/60),V.tab]"))
    await pg.evaluate("()=>{V.tab='c';render()}");await pg.click('[data-a=hrc]');await pg.wait_for_timeout(600)
    await pg.click('[data-a=lce]');await pg.wait_for_timeout(300);await pg.screenshot(path=O+'4-fine.png',full_page=True)
    await pg.click('[data-a=lcs]');await pg.wait_for_timeout(300)
    c=await pg.evaluate("()=>{const c=S.cd.find(c=>c.src=='live');return c&&{d:c.d,t:c.t,min:c.min,kc:c.kc,est:c.est,hr:c.hr,hz:c.hz,hs:c.hs.length}}");print('salvata',c)
    # import GPX sovrapposto -> Unisci
    await pg.set_input_files('#gxf',['/home/claude/w/gxs/live.gpx']);await pg.wait_for_timeout(800)
    print('dup',await pg.evaluate("()=>V.gi.L.map(a=>a.dup)"));await pg.screenshot(path=O+'5-unisci.png')
    await pg.click('[data-a=gisave]');await pg.wait_for_timeout(300)
    print('unita',await pg.evaluate("()=>{const L=S.cd.filter(c=>c.d==today());return L.map(c=>[c.t,c.min,c.km,c.kc,!!c.rte,!!c.hs,c.from])}"))
    await pg.evaluate("()=>{V.o.dCd=true;const c=S.cd.find(c=>c.src=='live');V.o['gxc_'+c.id]=true;render()}");await pg.wait_for_timeout(200)
    await (await pg.query_selector('#dCd')).screenshot(path=O+'6-storico.png')
    # seduta in palestra
    await pg.evaluate("()=>{V.ss={sid:'ssT',sc:'sA',fr:0,L:[],i:0,t0:Date.now()-50*60e3,d:today(),done:false};V.tab='ss';const t0=Date.now()-50*60e3;HRB=HRB.filter(x=>x[0]<t0);for(let i=0;i<50*60;i++)HRB.push([t0+i*1000,Math.round(100+30*Math.abs(Math.sin(i/90)))]);render()}")
    await pg.evaluate("()=>{HR.rs=152;tStart(90);scrollTo(0,0)}");await pg.wait_for_timeout(900);await pg.screenshot(path=O+"7-seduta.png")
    await pg.evaluate("()=>{tmHide();S.log.push({id:uid(),d:today(),e:S.sch[0].ex[0],kg:70,r:8,ss:'ssT'});ssEnd();render()}");await pg.wait_for_timeout(300)
    await pg.screenshot(path=O+'8-fine-seduta.png',full_page=True)
    print('ses',await pg.evaluate("()=>{const x=S.ses.find(s=>s.id=='ssT');return [x.hr,x.kc,x.hs.length]}"))
    # disconnessione e ricollegamento
    await pg.evaluate("()=>window.__bt.drop()");await pg.wait_for_timeout(200);print('drop',await pg.evaluate("()=>HR.st"));await pg.wait_for_timeout(2200);print('re',await pg.evaluate("()=>HR.st"))
    # senza bluetooth
    print('errs',errs);await b.close()
asyncio.run(main())
