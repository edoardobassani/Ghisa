# v250: scadenze proposte (chiusi almeno 7 giorni tranne il pesce fresco; aperti dalle fonti)
import gb,asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.add_init_script("if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','it')")
    await pg.goto(gb.URL);await pg.wait_for_timeout(500)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    r=await pg.evaluate("""()=>{const F=n=>allF().find(f=>f.name==n);const L=['Petto di pollo (crudo)','Macinato di manzo','Salmone','Merluzzo','Gamberi','Bresaola','Uovo intero','Latte parz. scremato','Yogurt greco 0%','Mozzarella','Parmigiano Reggiano','Spinaci','Zucchine','Fragole','Mela','Tonno al naturale','Passata di pomodoro','Pasta di semola (cruda)'];
      return L.map(n=>{const f=F(n);return f?[n,dsExp(f),dsOpenD(f)]:[n,'manca']})}""")
    for x in r:print(x)
    d={x[0]:x for x in r}
    ok(all((x[1]>=7 or x[1]==0) for x in r if x[0] not in('Salmone','Merluzzo','Gamberi') and x[1]!='manca'),'chiusi almeno 7 giorni (o senza scadenza)')
    ok(d['Salmone'][1]==2 and d['Merluzzo'][1]==2,'pesce fresco 2 giorni')
    ok(d['Latte parz. scremato'][2]==3 and d['Yogurt greco 0%'][2]==3 and d['Tonno al naturale'][2]==3 and d['Passata di pomodoro'][2]==5 and d['Bresaola'][2]==4,'aperti dalle fonti')
    ok(not E,'nessun errore JS '+str(E));await b.close()
asyncio.run(m())
