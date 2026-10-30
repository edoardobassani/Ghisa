import asyncio
from playwright.async_api import async_playwright
Q=['mozarella','parmiggiano','zuchine','prosciuto','bresaloa','yougurt','banan','philadelphia','phila','nutella','sottilette','insalata','cereali','evo','olio evo','whey','coca cola','uova','pollo','tacchino','sale','scatoletta','latte scremato','frutti di bosco','pizza',
   'olio','latte','pasta','riso','pane','mela','tonno','burro','ceci','fagioli','manzo','yogurt greco','petto di pollo','fiocchi di latte','grana','zucchine','spinaci','avocado','mandorle','biscotti']
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(600)
    for q in Q:
      r=await pg.evaluate("q=>{const t=performance.now();const L=(fMatch(q)||[]).slice(0,3).map(f=>f.name);const ms=performance.now()-t;const s=FSUG;const R=rtMatch(q).slice(0,2).map(x=>x.f.name);return [L.join(' ; '),s,R.join(' ; '),ms.toFixed(1)]}",q)
      print(f"{q:18}→ {r[0]}{'  [forse: '+r[1]+']' if r[1] else ''}  || ricetta: {r[2]}  ({r[3]}ms)")
    # UI check
    await pg.evaluate("()=>{V.tab='n';render()}");await pg.wait_for_timeout(200)
    await pg.evaluate("()=>{V.nd=today();render();document.querySelector('[data-a=mad][data-pm=Pranzo]').click()}");await pg.wait_for_timeout(300);inp=await pg.evaluate("()=>!!document.querySelector('#fq')")
    if inp:
      await pg.fill('#fq','mozarella');await pg.wait_for_timeout(400);await pg.screenshot(path='/home/claude/w/u/syn1.png')
      await pg.fill('#fq','philadelphia');await pg.wait_for_timeout(400);await pg.screenshot(path='/home/claude/w/u/syn2.png')
    print('input',inp,'errori',E)
    await b.close()
asyncio.run(m())
