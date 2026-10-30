import asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(700)
    print(await pg.evaluate("""()=>{const A=allF(),N=new Set(A.map(f=>f.name));const bad=[];Object.entries(FSYN).forEach(([k,v])=>v.forEach(n=>{if(!N.has(n))bad.push(k+'→'+n)}));
      const nw=A.filter(f=>MS[f.name]&&/^(Ciqual|USDA FoodData Central, SR|CREA, Tabelle di composizione degli alimenti \\(2019\\), codice)/.test(MS[f.name][0]));
      const ids=new Set();const dup=A.filter(f=>{if(ids.has(f.id))return true;ids.add(f.id)}).map(f=>f.name);
      const kc=nw.filter(f=>Math.abs(f.p*4+f.c*4+f.f*9-f.k)>Math.max(25,f.k*.2)).map(f=>f.name+' '+f.k+' vs '+Math.round(f.p*4+f.c*4+f.f*9));
      return {totale:A.length,nuovi:nw.length,sinonimiRotti:bad,duplicatiId:dup,kcalStrane:kc,cat:[...new Set(nw.map(cat))].length}}"""))
    for q in ['kefir','kefri','burata','burrata','pancarre','pan carrè','wrap','tortilla','semi di chia','sem di lino','tahini','quinoa','edamame','edamane','bulgur','bulgure','tiramisu','tiramisù','budino','red bull','coca zero','prosecco','spumante','songino','kale','cavolo nero','hipro','yogurt proteico','latte senza lattosio','granola','uvetta','uva passa','sushi','maki','hamburger','cotoletta','ravioli','tortellini','lasagne','bastoncini','dado','brodo','aceto','senape','ghee','papaya','papaia','melograno','more','lime','asiago','quark','surimi','polpette','mozzarella','pasta','olio','latte','pollo']:
      r=await pg.evaluate("q=>[(fMatch(q)||[]).slice(0,2).map(f=>f.name).join(' ; '),FSUG,rtMatch(q).slice(0,1).map(x=>x.f.name).join('')]",q)
      print(f"{q:22}→ {r[0]}{'  [forse: '+r[1]+']' if r[1] else ''} || ric: {r[2]}")
    # UI: info panel source of new food
    await pg.evaluate("()=>{V.tab='n';V.nd=today();render();document.querySelector('[data-a=mad][data-pm=Pranzo]').click()}");await pg.wait_for_timeout(300)
    await pg.fill('#fq','burrata');await pg.wait_for_timeout(300)
    await pg.evaluate("()=>document.querySelector('#fl [data-a=finf]').click()");await pg.wait_for_timeout(300)
    t=await pg.evaluate("()=>document.querySelector('.fin')?.innerText||''");print('INFO:',t.replace('\n',' | ')[-420:])
    await pg.screenshot(path='/home/claude/w/u/burrata.png',full_page=False)
    print('errori',E);await b.close()
asyncio.run(m())
