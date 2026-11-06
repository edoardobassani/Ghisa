# v222: chiudere a mano una giornata con poche calorie (Dieta e Home), che così entra nelle medie
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("""()=>{S.wc=1;S.goal=2000;const f=allF().find(x=>x.name=='Pane integrale'),add=(d,k,ms)=>ms.forEach(m=>S.meal.push({id:uid(),d,m,f:f.id,g:k/ms.length*100/f.k}));
      for(let i=8;i>=2;i--)add(hvAdd(today(),-i),2000,MPM);add(hvAdd(today(),-1),1000,['Colazione','Pranzo']);add(today(),2900,MPM);V.tab='n';V.nd=hvAdd(today(),-1);render()}""")
    print('regola: 1400 sì, 1399 no, 3000 sì:',await pg.evaluate("()=>[kcOk(1400),kcOk(1399),kcOk(3000)]"))
    print('Dieta, ieri sotto il 70%:',await pg.evaluate("()=>($('.dclw')||{}).innerText"))
    print('media 7 giorni prima:',await pg.evaluate("()=>{V.o.dn_kc=1;render();return $('#dn_kc h2').textContent}"))
    await pg.screenshot(path=O+'v222-avviso.png')
    await pg.click('.dclw [data-a=dcl]');await pg.wait_for_timeout(100)
    print('dopo chiusura:',await pg.evaluate("()=>[!!S.dcl[V.nd],($('.dclok')||{}).innerText,!$('.dclw'),!!document.querySelector('.dwk button.on .dclm')]"))
    print('media 7 giorni dopo:',await pg.evaluate("()=>$('#dn_kc h2').textContent+' · '+$('#dn_kc .hint').textContent"))
    await pg.screenshot(path=O+'v222-chiusa.png')
    print('pasti mancanti ora contano come non fatti:',await pg.evaluate("()=>mMiss(V.nd).length==0"))
    await pg.click('[data-a=dclr]');print('riaperta:',await pg.evaluate("()=>[!S.dcl[V.nd],!!$('.dclw')]"))
    # oggi: niente avviso anche se sotto il 70%
    await pg.evaluate("()=>{V.nd=today();S.meal=S.meal.filter(m=>m.d!=today());const f=allF().find(x=>x.name=='Pane integrale');S.meal.push({id:uid(),d:today(),m:'Colazione',f:f.id,g:100});render()}")
    print('oggi niente avviso:',await pg.evaluate("()=>!$('.dclw')"))
    # Home: riquadro Ieri
    await pg.evaluate("()=>{V.tab='h';render()}")
    print('Home ieri:',await pg.evaluate("()=>{const w=$('.card .dclw');return w?w.innerText.replace(/\\n/g,' | '):'nessuno'}"))
    await pg.click('.card .dclw [data-a=dclg]');print('Apri il diario:',await pg.evaluate("()=>[V.tab,V.nd==hvAdd(today(),-1)]"))
    await pg.evaluate("()=>{V.tab='h';render()}");await pg.click('.card .dclw [data-a=dcl]')
    print('Home dopo chiusura, niente riquadro né avvisi dei pasti:',await pg.evaluate("()=>!$('.card .dclw')&&!$('.ogmiss')"))
    print('errori',E);await b.close()
asyncio.run(m())
