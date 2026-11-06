# v232: «Anche nella scheda» in seduta resta anche nei programmi a blocchi (le schede si rigenerano ogni settimana)
import gb,asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    r=await pg.evaluate("""()=>{S.wc=1;const o={};xbAdd(['Panca piana bilanciere','Squat','Panca piana manubri','Dip']);const id=n=>S.ex.find(e=>e.name==n).id;
     S.sch.push({id:'A',name:'A',ex:[id('Panca piana bilanciere'),id('Squat')],t:{},rt:{},ss:[]});
     V.ss={sc:'A',d:today(),st:{},i:0};swDo(id('Panca piana bilanciere'),id('Panca piana manubri'),'sch');o.normale=S.sch.find(x=>x.id=='A').ex.map(nm).join(',');
     V.ss={sc:'A',d:today(),st:{},i:0};swDo(id('Squat'),id('Dip'),'oggi');o.soloOggi=S.sch.find(x=>x.id=='A').ex.map(nm).join(',');
     const p=bpStart(bpRes(BPM.find(x=>x[0]=='ppl')[1]()),[0,2,4]),sc=S.sch.find(x=>x.id==p.sch[0]),old=sc.ex[0];
     V.ss={sc:sc.id,d:today(),st:{},i:0};swDo(old,id('Dip'),'sch');o.bpSubito=nm(sc.ex[0]);bpNext(1);o.bpSettimanaDopo=nm(S.sch.find(x=>x.id==p.sch[0]).ex[0]);o.vecchio=nm(old);return o}""")
    print(r)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    ok(r['normale']=='Panca piana manubri,Squat','scheda normale: sostituito nella scheda')
    ok(r['soloOggi']=='Panca piana manubri,Squat','«Solo oggi» non tocca la scheda')
    ok(r['bpSubito']=='Dip','programma a blocchi: sostituito subito')
    ok(r['bpSettimanaDopo']=='Dip','programma a blocchi: resta anche la settimana dopo (era '+r['vecchio']+')')
    print('errori:',E);await b.close()
asyncio.run(m())
