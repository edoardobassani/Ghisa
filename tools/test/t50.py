# v211: modifica dei grammi delle voci del piano pasti (un giorno o tutti i giorni con la stessa voce)
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/'
srv=subprocess.Popen(['python3','-m','http.server','8786','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8786/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='pp';render()}");await pg.set_input_files('#ipf','pdft/nutrium_circ.pdf');await pg.wait_for_timeout(1800)
    for s in ['2','3']:await pg.click(f'[data-a=ipgo][data-s="{s}"]')
    await pg.click('[data-a=ipok]');await pg.wait_for_timeout(200)
    olio="()=>[0,1,2,3,4,5,6].map(d=>ppD(d).Pranzo.find(x=>/Olio/.test(fo(x.f).name)).g).join(',')"
    await pg.evaluate("()=>{const x=ppD(V.pj).Pranzo.find(x=>/Olio/.test(fo(x.f).name));document.querySelector(`[data-a=ppge][data-i=\"${x.id}\"]`).click()}");await pg.wait_for_timeout(150)
    print('modifica aperta:',await pg.evaluate("()=>[!!document.querySelector('#ppeg'),document.querySelector('#ppeg').value,document.querySelector('#ppek').textContent,!!document.querySelector('#ppea'),document.activeElement.id]"))
    await pg.click('[data-a=ppgm][data-s="1"]');print('dopo +:',await pg.evaluate("()=>[document.querySelector('#ppeg').value,document.querySelector('#ppek').textContent]"))
    await pg.fill('#ppeg','15');await pg.wait_for_timeout(50);print('kcal mentre scrivo:',await pg.evaluate("()=>document.querySelector('#ppek').textContent"))
    await pg.screenshot(path=O+'ppe.png',full_page=True)
    await pg.click('[data-a=ppgs]');await pg.wait_for_timeout(150);print('solo oggi:',await pg.evaluate(olio),await pg.evaluate("()=>document.querySelector('#toast').textContent"))
    await pg.click('#undo button');await pg.wait_for_timeout(150);print('annulla:',await pg.evaluate(olio))
    await pg.evaluate("()=>{const x=ppD(V.pj).Pranzo.find(x=>/Olio/.test(fo(x.f).name));document.querySelector(`[data-a=ppge][data-i=\"${x.id}\"]`).click()}");await pg.fill('#ppeg','8');await pg.check('#ppea');await pg.click('[data-a=ppgs]');await pg.wait_for_timeout(150)
    print('tutti i giorni:',await pg.evaluate(olio),await pg.evaluate("()=>document.querySelector('#toast').textContent"))
    # voce con alternative: le alternative seguono i grammi della voce attiva
    await pg.evaluate("()=>{const x=ppD(V.pj).Pranzo.find(x=>x.al&&x.al.length==6);document.querySelector(`[data-a=ppge][data-i=\"${x.id}\"]`).click()}");await pg.fill('#ppeg','100');await pg.click('[data-a=ppgs]');await pg.wait_for_timeout(150)
    print('pasta con alternative:',await pg.evaluate("()=>{const x=ppD(V.pj).Pranzo.find(x=>x.al&&x.al.length==6);return x.g+' | '+x.al.map(a=>fo(a.f).name.split(' ')[0]+' '+a.g).join(', ')+' | scambiato:'+mpSwd(x)}"))
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
