# v224: attrezzatura di ogni esercizio (catalogo, esercizi personali, guida, foglio di modifica)
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O;os.makedirs(O,exist_ok=True)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    print('catalogo coperto:',await pg.evaluate("()=>XBL.filter(x=>!ATX[x.name]).map(x=>x.name)"))
    print('esempi:',await pg.evaluate("()=>['Panca piana bilanciere','Lat machine','Squat bulgaro','Trazioni','Crunch'].map(n=>n+': '+atTxt(atOf({name:n}).o))"))
    print('atOk casa (b,m,p,s):',await pg.evaluate("()=>['Panca piana bilanciere','Lat machine','Rematore manubrio','Leg press','Dip','Face pull','Glute bridge'].map(n=>n+':'+atOk({name:n},'bmps'))"))
    print('nomi non del catalogo:',await pg.evaluate("()=>['Panca piana con manubri','Shoulder press al cavo','Leg press 45°','Trazioni zavorrate','Esercizio strano'].map(n=>n+': '+((a=>a?atTxt(a.o):'sconosciuta')(atOf({name:n}))))"))
    await pg.evaluate("()=>{S.wc=1;xbAdd(['Panca piana bilanciere','Lat machine','Squat bulgaro']);V.tab='e';V.o['ge_Petto']=1;render()}")
    print('riga in Esercizi:',await pg.evaluate("()=>[...document.querySelectorAll('.cxr2 .hint')].map(x=>x.textContent).slice(0,3)"))
    print('guida:',await pg.evaluate("()=>{const id=S.ex.find(e=>e.name=='Squat bulgaro').id;const d=document.createElement('div');d.innerHTML=gdBox(id);return d.querySelector('h4').textContent+': '+d.querySelector('p').textContent}"))
    # esercizio personale con attrezzatura
    await pg.click('[data-a=exnt]');await pg.fill('#exn2','Panca landmine');await pg.click('[data-a=exat][data-v=b]');await pg.click('[data-a=exat][data-v=p]')
    print('scelta:',await pg.evaluate("()=>V.exf.eq"));await pg.screenshot(path=O+'v224-foglio.png');await pg.click('[data-a=exok]')
    print('salvato:',await pg.evaluate("()=>{const e=S.ex.find(x=>x.name=='Panca landmine');return [e.eq,atTxt(atOf(e).o)]}"))
    # modifica di un esercizio del catalogo: se non cambi niente non salva eq
    await pg.evaluate("()=>{const id=S.ex.find(e=>e.name=='Lat machine').id;exSheet(id)}");await pg.click('[data-a=exok]')
    print('catalogo invariato senza eq:',await pg.evaluate("()=>S.ex.find(e=>e.name=='Lat machine').eq===undefined"))
    await pg.evaluate("()=>{const id=S.ex.find(e=>e.name=='Lat machine').id;exSheet(id)}");await pg.click('[data-a=exat][data-v=e]');await pg.click('[data-a=exok]')
    print('catalogo cambiato:',await pg.evaluate("()=>{const e=S.ex.find(e=>e.name=='Lat machine');return [e.eq,atTxt(atOf(e).o)]}"))
    await pg.evaluate("()=>{xbOpen()}");await pg.wait_for_timeout(100);print('catalogo mostra attrezzatura:',await pg.evaluate("()=>document.querySelector('#xbl .sdi span small').textContent"))
    await pg.screenshot(path=O+'v224-catalogo.png')
    print('errori',E);await b.close()
asyncio.run(m())
