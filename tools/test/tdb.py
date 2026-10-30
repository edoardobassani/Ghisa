import asyncio,json
from playwright.async_api import async_playwright
F='file://'+__import__('os').environ.get('SRC','/home/claude/w/tracker-palestra.html')+''
async def page(b,init=None):
  ctx=await b.new_context();pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  if init:await pg.add_init_script(init)
  return ctx,pg,errs
st="()=>({dbm:DBM,ex:S.ex.length,ls:!!localStorage.getItem('ghisa'),old:!!localStorage.getItem('ghisa-old'),wal:!!localStorage.getItem('ghisa-wal'),v:document.querySelector('#v').innerText.slice(0,30)})"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    # 1 nuovo utente
    ctx,pg,e=await page(b);await pg.goto(F);await pg.wait_for_timeout(500)
    print('1 nuovo',await pg.evaluate(st))
    await pg.evaluate("()=>{xbAdd(['Squat']);save()}");await pg.wait_for_timeout(300);await pg.reload();await pg.wait_for_timeout(500)
    print('1 dopo salvataggio e riavvio',await pg.evaluate(st),e)
    # 2 chiusura immediata: salva e ricarica subito
    await pg.evaluate("()=>{xbAdd(['Lat machine']);save();location.reload()}");await pg.wait_for_timeout(800)
    print('2 ricarica immediata',await pg.evaluate(st),e)
    await ctx.close()
    # 3 migrazione da localStorage
    ctx,pg,e=await page(b);await pg.goto(F);await pg.wait_for_timeout(300)
    await pg.evaluate("()=>{indexedDB.deleteDatabase('ghisa-dati');localStorage.setItem('ghisa',JSON.stringify({ex:[{id:'a',name:'Panca piana bilanciere',g:'Petto'}],sch:[],log:[{id:'l1',d:'2026-10-01',e:'a',kg:60,r:8}],meal:[],svd:5}))}")
    await pg.reload();await pg.wait_for_timeout(700)
    print('3 migrazione',await pg.evaluate(st),e)
    await pg.reload();await pg.wait_for_timeout(500)
    print('3 riavvio dopo migrazione',await pg.evaluate(st),await pg.evaluate("()=>S.log.length"))
    # 4 localStorage più recente (vecchia versione dell'app in cache)
    await pg.evaluate("()=>{const o=JSON.parse(JSON.stringify(S));o.ex.push({id:'b',name:'Squat',g:'Quadricipiti'});o.svd=Date.now()+1e6;localStorage.setItem('ghisa',JSON.stringify(o))}")
    await pg.reload();await pg.wait_for_timeout(600)
    print('4 ls più recente',await pg.evaluate(st))
    # 5 cancella tutto
    await pg.evaluate("()=>{window.confirm=()=>true;const b=document.createElement('button');b.dataset.a='wipe';document.body.append(b);b.click();const y=[...document.querySelectorAll('#cfm button')].find(x=>/cancella/i.test(x.textContent)&&x.dataset.a!='wipe');return y?y.dataset.a:'nessun tasto'}")
    a=await pg.evaluate("()=>[...document.querySelectorAll('#cfm button')].map(x=>x.dataset.a+':'+x.textContent).join(' | ')");print('5 dialogo',a)
    await ctx.close()
    # 6 senza IndexedDB
    ctx,pg,e=await page(b,"Object.defineProperty(window,'indexedDB',{value:undefined})");await pg.goto(F);await pg.wait_for_timeout(400)
    await pg.evaluate("()=>{xbAdd(['Squat']);save()}");await pg.reload();await pg.wait_for_timeout(400)
    print('6 senza IDB',await pg.evaluate(st),e)
    await ctx.close();await b.close()
asyncio.run(main())
