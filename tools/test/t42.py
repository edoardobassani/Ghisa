# v203: codice a barre → grammi e pasto subito (prodotto nuovo da Open Food Facts e prodotto già salvato)
import gb
import asyncio,subprocess,time,os
from playwright.async_api import async_playwright
SRC=gb.SRC;W=gb.D;O=gb.O
FAKE="""window.__n=0;window.BarcodeDetector=class{constructor(){}async detect(){window.__n++;return window.__n%10==0?[{rawValue:'8001234567897'}]:[]}}"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    ctx=await b.new_context(viewport={'width':390,'height':844},permissions=['camera']);await ctx.add_init_script(FAKE)
    await ctx.route('**/world.openfoodfacts.org/**',lambda r:r.fulfill(json={'status':1,'product':{'product_name':'Biscotti prova','brands':'Marca','nutriments':{'energy-kcal_100g':450,'proteins_100g':7,'carbohydrates_100g':70,'fat_100g':15}}}))
    pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto(gb.URL);await pg.wait_for_timeout(800)
    await pg.evaluate("()=>{S.wc=1;V.tab='n';V.nd=today();V.mm='Colazione';render();bcOpen()}");await pg.wait_for_timeout(3500)
    print('nuovo:',await pg.evaluate("()=>[!!document.querySelector('#bq_g'),document.querySelector('#bq_g').value,document.querySelector('#bq_m').value,document.querySelector('#bq_s').textContent]"))
    await pg.screenshot(path=O+'bc-add.png',full_page=True)
    await pg.fill('#bq_g','40');await pg.click('#bq_s');await pg.wait_for_timeout(300)
    print('aggiunto:',await pg.evaluate("()=>[document.querySelector('#toast').textContent,S.meal.map(x=>fo(x.f).name+' '+x.g+' '+x.m+' '+x.d),!document.querySelector('#bco'),V.tab]"))
    await pg.evaluate("()=>{window.__n=0;V.mm='Spuntino';bcOpen()}");await pg.wait_for_timeout(3500)
    print('già salvato:',await pg.evaluate("()=>[document.querySelector('#bcm').textContent,document.querySelector('#bq_g').value,document.querySelector('#bq_m').value,!!document.querySelector('#bq_a')]"))
    await pg.screenshot(path=O+'bc-known.png')
    await pg.click('#bq_a');await pg.wait_for_timeout(300)
    print('aggiunto di nuovo:',await pg.evaluate("()=>S.meal.map(x=>fo(x.f).name+' '+x.g+' '+x.m)"))
    print('errori',E);await b.close()
asyncio.run(m())
