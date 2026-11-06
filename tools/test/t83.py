# v246: dispensa (scarico dal diario, Casa/Fuori, cotto→crudo, ricette, finito, spesa, controllo, generatore)
import gb,asyncio,json
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    await pg.evaluate("(d)=>{norm(JSON.parse(d));S.dsp=null;S.mfo={};save()}",D);await pg.reload();await pg.wait_for_timeout(700)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    F="(n)=>allF().find(f=>f.name==n).id"
    # aggiunta dalla dispensa
    await pg.evaluate("()=>{V.tab='pp';V.pv='d';render()}");await pg.wait_for_timeout(200)
    await pg.type('#dsq','pasta di semola',delay=20);await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{const id=allF().find(f=>f.name=='Pasta di semola (cruda)').id;document.querySelector('[data-a=dsa][data-i=\"'+id+'\"]').click()}");await pg.wait_for_timeout(200)
    await pg.fill('#dsg','500');await pg.click('[data-a=dsok]');await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;dsPut(a('Passata di pomodoro'),700);dsPut(a('Petto di pollo (crudo)'),100);dsPut(a('Yogurt greco 0%'),500);dsPut(a('Riso (crudo)'),1000);save();render()}");await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[dsN(),document.querySelectorAll('.dsi').length]");ok(r[0]==5 and r[1]==5,'5 alimenti in dispensa '+str(r))
    await pg.screenshot(path=gb.O+'ds1.png',full_page=True)
    # pasto a casa: pasta cotta → cruda + avviso
    await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n);const pc=a('Pasta (cotta)')||allF().find(f=>/^pasta.*cott/i.test(f.name));V.tab='n';V.nd=today();S.meal.push({id:uid(),d:today(),m:'Cena',f:pc.id,g:200},{id:uid(),d:today(),m:'Cena',f:a('Passata di pomodoro').id,g:100});save();render()}");await pg.wait_for_timeout(400)
    r=await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;return [Math.round(dsLeft(a('Pasta di semola (cruda)'))),dsLeft(a('Passata di pomodoro')),($('#dstst')||{}).innerText]}");print(r)
    ok(390<r[0]<420 and r[1]==600,'cotto→crudo e passata scalati');ok(r[2] and 'Tolti' in r[2],'avviso dopo il pasto')
    await pg.screenshot(path=gb.O+'ds2.png')
    await pg.click('[data-a=dstf]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;return [dsLeft(a('Pasta di semola (cruda)')),mFuori(today(),'Cena')]}");ok(r[0]==500 and r[1],'«Era fuori casa» rimette tutto '+str(r))
    await pg.click('[data-a=dsfo][data-pm=Cena][data-v="0"]');await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;return Math.round(dsLeft(a('Pasta di semola (cruda)')))}");ok(r<420,'«Casa» toglie di nuovo')
    # fuori casa su un pasto
    await pg.click('[data-a=dsfo][data-pm=Pranzo][data-v="1"]');await pg.wait_for_timeout(150)
    await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id;S.meal.push({id:uid(),d:today(),m:'Pranzo',f:a('Riso (crudo)'),g:100});save();render()}");await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[dsLeft(allF().find(f=>f.name=='Riso (crudo)').id),!!document.querySelector('.dsfb')]");ok(r[0]==1000 and r[1],'pasto fuori: dispensa invariata, scritta visibile')
    await pg.screenshot(path=gb.O+'ds3.png',full_page=True)
    # annulla
    await pg.evaluate("()=>{S.meal.push({id:uid(),d:today(),m:'Colazione',f:allF().find(f=>f.name=='Yogurt greco 0%').id,g:170});save();render()}");await pg.wait_for_timeout(300)
    await pg.click('[data-a=dstu]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>dsLeft(allF().find(f=>f.name=='Yogurt greco 0%').id)")==500,'Annulla: dispensa invariata, pasto resta')
    # finito
    await pg.evaluate("()=>{S.meal.push({id:uid(),d:today(),m:'Pranzo',f:allF().find(f=>f.name=='Petto di pollo (crudo)').id,g:150});S.mfo[today()+'|Pranzo']=0;save();render()}");await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[dsLeft(allF().find(f=>f.name=='Petto di pollo (crudo)').id),!!document.querySelector('.dsz')]");ok(r[0]==0 and r[1],'finito: zero, non sotto, con avviso')
    await pg.click('.dsz [data-a=dsz]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>S.spx.some(v=>v.t=='Petto di pollo (crudo)')"),'«Aggiungi alla spesa»')
    # ricetta
    r=await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n);const rc={id:'rTST',name:'Pasta al pomodoro di casa',k:150,p:5,c:28,f:2,rc:{it:[{f:a('Pasta di semola (cruda)').id,g:320},{f:a('Passata di pomodoro').id,g:400}],w:1200}};S.food.push(rc);const b=dsLeft(a('Passata di pomodoro').id);S.meal.push({id:uid(),d:today(),m:'Cena',f:'rTST',g:300});DSC=null;return [b,dsLeft(a('Passata di pomodoro').id)]}")
    ok(r[0]-r[1]==100,'ricetta: ingredienti in proporzione '+str(r))
    # spesa
    await pg.evaluate("()=>{const a=n=>allF().find(f=>f.name==n).id,w=hvMon(today());S.mpw[w]={0:{Pranzo:[{id:'x1',gid:'x1',f:a('Riso (crudo)'),g:80},{id:'x2',gid:'x2',f:a('Zucchine'),g:200}]},1:{Pranzo:[{id:'x3',gid:'x3',f:a('Riso (crudo)'),g:80},{id:'x4',gid:'x4',f:a('Ceci in scatola'),g:150}]}};V.pw=w;dsPut(a('Ceci in scatola'),100);V.tab='pp';V.pv='s';V.psd=null;render()}");await pg.wait_for_timeout(200)
    r=await pg.evaluate("()=>[!!document.querySelector('.dshc'),document.querySelector('#v').innerText.includes('ne hai')]");print(r);ok(r[0] or r[1],'spesa tiene conto della dispensa')
    n=await pg.evaluate("()=>{const o=ppSpesa();dsSp(o);const k=Object.keys(o)[0];S.mc[k]=1;render();return fo(k).name}")
    await pg.click('[data-a=dsbuy]');await pg.wait_for_timeout(200);ok(await pg.evaluate(f"()=>!!S.dsp.it[allF().find(f=>f.name=={json.dumps(n)}).id]"),'«Ho fatto la spesa» mette in dispensa')
    await pg.screenshot(path=gb.O+'ds4.png',full_page=True)
    # controllo settimanale
    await pg.evaluate("()=>{S.dsp.ck=dShift(today(),-8);V.pv='d';render()}");await pg.wait_for_timeout(200)
    ok(await pg.evaluate("()=>!!document.querySelector('.dsck')"),'controllo veloce dopo 7 giorni')
    await pg.click('.dsck [data-a=dckv][data-v=f] >> nth=0');await pg.click('[data-a=dcks]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>S.dsp.ck==today()&&!document.querySelector('.dsck')"),'controllo salvato')
    await pg.screenshot(path=gb.O+'ds5.png',full_page=True)
    # abitudine fuori casa
    r=await pg.evaluate("()=>{for(let i=0;i<14;i++){const d=dShift(today(),-i),w=new Date(d+'T12:00:00').getDay();if(w>=1&&w<=5)S.mfo[d+'|Pranzo']=1}V.dsaf=null;delete S.dsp.afn.Pranzo;dsHabitChk('Pranzo');return V.dsaf}");ok(r=='Pranzo','proposta pranzi feriali fuori casa')
    # modalità chiedi
    await pg.evaluate("()=>{S.dsp.mode='c';DSS=null;V.tab='n';render()}");await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{dsPut(allF().find(f=>f.name=='Lenticchie lesse').id,400);S.meal.push({id:uid(),d:today(),m:'Spuntino',f:allF().find(f=>f.name=='Lenticchie lesse').id,g:50});render()}");await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>[($('#dstst')||{}).innerText,dsLeft(allF().find(f=>f.name=='Lenticchie lesse').id)]");print(r);ok('Togli dalla dispensa?' in (r[0] or '') and r[1]==400,'«Chiedi ogni volta» non toglie finché non confermi')
    await pg.click('[data-a=dsty]');await pg.wait_for_timeout(150);ok(await pg.evaluate("()=>dsLeft(allF().find(f=>f.name=='Lenticchie lesse').id)")==350,'confermato: tolto')
    # generatore usa la dispensa
    await pg.evaluate("()=>{S.dsp.mode='a';const a=n=>allF().find(f=>f.name==n).id;dsPut(a('Spinaci'),300,dShift(today(),1));dsPut(a('Ceci in scatola'),800);V.tab='pp';mgOpen({st:'gen'});render()}");await pg.wait_for_timeout(300)
    r=await pg.evaluate("()=>{const N=V.mg.G.W.flatMap(D=>MP.flatMap(m=>(D[m]||[]).map(y=>[y.n,y.why])));return [N.filter(x=>x[0]=='Spinaci').length,N.filter(x=>/dispensa|scad/.test(x[1]||'')).length]}");print(r);ok(r[0]>=1 and r[1]>=3,'generatore: alimenti in dispensa preferiti, col motivo')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
