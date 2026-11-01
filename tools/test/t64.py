# v227: costruttore nella pagina Schede; sezione Integratori
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
SEED="""(veg)=>{S.wc=1;S.goal=2200;S.pf={sx:'m',age:38};S.wt=[{id:'w1',d:hvAdd(today(),-2),kg:80}];S.meal=[];S.log=[];S.cd=[];
 const F=n=>allF().find(f=>f.name==n),M=veg?[['Colazione','Fiocchi d’avena',80],['Pranzo','Pasta di semola (cruda)',120],['Pranzo','Lenticchie secche',80],['Cena','Riso (crudo)',100],['Cena','Ceci secchi',80],['Spuntini','Banana',150],['Spuntini','Mandorle',30],['Cena','Pane integrale',150],['Pranzo','Olio extravergine d’oliva',30]]
  :[['Colazione','Fiocchi d’avena',80],['Pranzo','Pasta di semola (cruda)',120],['Pranzo','Petto di pollo (crudo)',150],['Cena','Riso (crudo)',100],['Cena','Uovo intero',100],['Spuntini','Banana',150],['Cena','Pane integrale',100],['Pranzo','Olio extravergine d’oliva',30]];
 for(let i=1;i<=21;i++){const d=hvAdd(today(),-i);M.forEach(([m,n,g])=>{const f=F(n);if(f)S.meal.push({id:uid(),d,m,f:f.id,g})});if(i%2&&!veg){}if(i%7==3&&!veg)S.meal.push({id:uid(),d,m:'Cena',f:F('Salmone').id,g:150});
  if(i%7<3){S.log.push({id:uid(),d,e:'x',kg:60,r:8})}if(i%7==5)S.cd.push({id:uid(),d,t:'Corsa',min:90})}
 ['Fiocchi d’avena','Lenticchie secche','Mandorle','Banana','Pasta di semola (cruda)','Riso (crudo)','Ceci secchi','Pane integrale','Olio extravergine d’oliva','Petto di pollo (crudo)','Uovo intero','Salmone'].forEach(n=>{if(!F(n))console.log('manca',n)});
 V.tab='it';render()}"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('console',lambda c:E.append(c.text) if 'manca' in c.text else None)
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='s';render()}")
    print('hero in Schede:',await pg.evaluate("()=>[!!$('#v > .pbhero, #v .pbhero'),$('.pbhero b').textContent]"))
    await pg.click('.pbhero');print('aperto:',await pg.evaluate("()=>[V.pb.st,$('[data-a=pbx]').textContent]"))
    await pg.click('[data-a=pbx]');print('torna a Schede:',await pg.evaluate("()=>[!V.pb,!V.pg,!!$('.pbhero')]"))
    await pg.click('[data-a=pgl]');print('non più in Programmi pronti:',await pg.evaluate("()=>!$('.pbhero')"))
    await pg.evaluate(SEED,False);await pg.wait_for_timeout(100)
    r=await pg.evaluate("()=>{const D=itData();return {n:D.n,gym:D.gym,cd:D.cd,ty:D.ty,pg:Math.round(D.pg*100)/100,fish:D.fish,cov:Math.round(D.cov*100),avg:D.avg&&D.avg.map(Math.round),L:itList(D).map(o=>o.k+':'+o.t)}}");print('onnivoro:',r)
    await pg.screenshot(path=O+'v227-onn.png',full_page=True)
    await pg.click('[data-a=itg][data-k=cre]');print('lo prendo:',await pg.evaluate("()=>[S.itg,[...document.querySelectorAll('.ith2')].map(x=>x.textContent)]"))
    await pg.evaluate(SEED,True);await pg.wait_for_timeout(100)
    r=await pg.evaluate("()=>{const D=itData();return {ty:D.ty,pg:Math.round(D.pg*100)/100,L:itList(D).map(o=>o.k+':'+o.t+(o.foods?'['+o.foods.join('/')+']':''))}}");print('vegano:',r)
    await pg.screenshot(path=O+'v227-veg.png',full_page=True)
    print('menu:',await pg.evaluate("()=>[...document.querySelectorAll('nav button[data-t=it], [data-t=it]')].length"))
    await pg.evaluate("()=>{V.tab='n';V.nd=hvAdd(today(),-1);V.o.dMi=true;render()}");print('link da Dieta:',await pg.evaluate("()=>!!$('#dMi [data-t=it]')"))
    print('errori:',E);await b.close()
asyncio.run(m());srv.terminate()
