# v196: tasto ⇄ sulle voci del piano (alternative del piano + equivalenti), solo un giorno o tutti, Home
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8773','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8773/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='pp';render()}");await pg.set_input_files('#ipf','pdft/nutrium_circ.pdf');await pg.wait_for_timeout(1800)
    for s in ['2','3']:await pg.click(f'[data-a=ipgo][data-s="{s}"]')
    await pg.click('[data-a=ipok]');await pg.wait_for_timeout(300)
    di=await pg.evaluate("()=>V.pj");W=await pg.evaluate("()=>V.pw||hvMon(today())")
    print('chip nel piano:',await pg.evaluate("()=>[...document.querySelectorAll('#v .swc')].map(b=>b.textContent).join(' ')"))
    await pg.screenshot(path=O+'sw-pp.png',full_page=True)
    # apri ⇄ sulla pasta del pranzo
    await pg.evaluate("()=>{const it=ppD(V.pj).Pranzo.find(x=>x.al&&x.al.length==6);document.querySelector(`[data-a=mpso][data-i=\"${it.id}\"]`).click()}");await pg.wait_for_timeout(200)
    print('foglio:',await pg.evaluate("()=>[...document.querySelectorAll('#cfm .xsec')].map(e=>e.textContent)+' | '+[...document.querySelectorAll('#cfm .xpo')].length+' righe | '+[...document.querySelectorAll('#cfm [data-a=mpss]')].map(e=>e.textContent).join('/')"))
    await pg.screenshot(path=O+'sw-sheet.png')
    await pg.click('#cfm [data-a=mpss][data-v="1"]')
    await pg.evaluate("()=>{const r=allF().find(x=>x.name=='Riso (crudo)');document.querySelector(`#cfm [data-a=mpsw][data-f=\"${r.id}\"]`).click()}");await pg.wait_for_timeout(200)
    print('toast:',await pg.evaluate("()=>document.querySelector('#toast').textContent"))
    print('pranzo nei 7 giorni:',await pg.evaluate("()=>[0,1,2,3,4,5,6].map(d=>{const it=ppD(d).Pranzo.find(x=>x.al&&x.al.length==6);return fo(it.f).name.split(' ')[0]+(mpSwd(it)?'*':'')}).join(' ')"))
    await pg.click('#undo button');await pg.wait_for_timeout(200)
    print('dopo Annulla:',await pg.evaluate("()=>[0,1,2,3,4,5,6].map(d=>fo(ppD(d).Pranzo.find(x=>x.al&&x.al.length==6).f).name.split(' ')[0]).join(' ')"))
    # solo oggi, su una voce senza alternative (olio): diventa scambiata e crea al
    await pg.evaluate("()=>{const it=ppD(V.pj).Pranzo.find(x=>!x.al);document.querySelector(`[data-a=mpso][data-i=\"${it.id}\"]`).click()}");await pg.wait_for_timeout(200)
    print('senza alt:',await pg.evaluate("()=>[...document.querySelectorAll('#cfm .xsec')].map(e=>e.textContent).join(',')+' | '+[...document.querySelectorAll('#cfm .xpo')].map(e=>e.textContent.slice(0,30)).join(' / ')"))
    await pg.evaluate("()=>document.querySelector('#cfm [data-a=mpsa]').click()");await pg.wait_for_timeout(200)
    print('+⇄:',await pg.evaluate("()=>[document.querySelector('#toast').textContent,[...document.querySelectorAll('#cfm .xsec')].map(e=>e.textContent).join(',')]"))
    await pg.evaluate("()=>{const b=[...document.querySelectorAll('#cfm [data-a=mpsw]')].find(b=>!b.classList.contains('on'));b.click()}");await pg.wait_for_timeout(200)
    print('pranzo oggi:',await pg.evaluate("()=>ppD(V.pj).Pranzo.map(x=>fo(x.f).name+' '+x.g+(mpSwd(x)?' [scambiato]':'')+(x.al?' al'+x.al.length:''))"))
    # Home
    await pg.evaluate("()=>{V.tab='h';V.ogsel='Pranzo';V.ogseld=today();render()}");await pg.wait_for_timeout(200)
    print('home:',await pg.evaluate("()=>[...document.querySelectorAll('.ogl li')].map(l=>l.textContent).join(' | ')"))
    await pg.evaluate("()=>{const b=document.querySelector('.ogl [data-a=mpso]');b&&b.click()}");await pg.wait_for_timeout(200)
    print('foglio da Home:',await pg.evaluate("()=>!!document.querySelector('#cfm.sht .swh')"))
    await pg.screenshot(path=O+'sw-home.png');await pg.click('#cfm [data-a=cfx]')
    await pg.screenshot(path=O+'sw-home2.png',full_page=True)
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
