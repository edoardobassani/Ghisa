# v228: correzioni dalla verifica delle fonti
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    r=await pg.evaluate("""()=>{S.wc=1;const o={};S.pf={sx:'m',age:70};o.na70=miL()[0][2];S.pf.age=40;o.na40=miL()[0][2];
     o.walk5=cdMet('Camminata',60,5);o.walk4=cdMet('Camminata',60,4);o.bike=cdMet('Bici',60,0);o.bike9=cdMet('Bici',60,8.9);o.run10=cdMet('Corsa',60,10.8);
     const f=allF().find(x=>x.name=='Sale');o.sale=microOf(f)[0];
     xbAdd(['Squat']);const id=S.ex.find(e=>e.name=='Squat').id;S.log=[{id:'a',d:hvAdd(today(),-3),e:id,kg:100,r:12}];o.rm=Math.round(rmOf(id).kg*10)/10;o.rm1=Math.round(rm1(100,12)*10)/10;
     const D={...itData(),ty:'n',n:10,kg:70,avg:Array(9).fill(80)};o.b12=itList(D).find(x=>x.k=='b12');o.b12=o.b12&&[o.b12.t,o.b12.ev||null];
     S.pf.age=70;o.ptg=itData().ptg;return o}""");print(r)
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
