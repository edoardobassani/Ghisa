# v233: lingua dell'app (inglese e francese) — copertura delle traduzioni, ricerca cibi, cambio lingua
import gb,asyncio,re,sys
from collections import Counter
from playwright.async_api import async_playwright
D=open(gb.REPO+'/tools/demo/demo_data.json').read()
IT=re.compile(r"\b(di|della|delle|scheda|schede|serie|esercizi|esercizio|allenamento|allenamenti|settimana|giorni|oggi|tocca|aggiungi|nessun|nessuna|il|con|più|sono|anche|ancora|pasto|pasti|seduta|sedute|uscita|uscite|ripetizioni|fatto|fatta|cerca|salva|elimina|modifica)\b",re.I)
TABS=['h','w','c','s','e','g','n','it','p','o','inf','gd']
async def lang(b,l,rep):
  pg=await b.new_page(viewport={'width':390,'height':844});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  await pg.add_init_script(f"try{{if(!localStorage.getItem('gb-lang'))localStorage.setItem('gb-lang','{l}')}}catch(e){{}}")
  await pg.goto(gb.URL);await pg.wait_for_timeout(500)
  await pg.evaluate("(d)=>{norm(JSON.parse(d));save()}",D);await pg.reload();await pg.wait_for_timeout(700)
  C=Counter()
  for t in TABS:
    await pg.evaluate(f"()=>{{V.tab='{t}';document.querySelectorAll('details').forEach(d=>d.open=true);render();document.querySelectorAll('#v details').forEach(d=>d.open=true)}}");await pg.wait_for_timeout(250)
    tx=await pg.evaluate("()=>{const o=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const p=n.parentElement;if(!p||/SCRIPT|STYLE/.test(p.tagName)||p.closest('.notr'))continue;const v=n.nodeValue.replace(/\\s+/g,' ').trim();if(v)o.push(v)}return o}")
    for v in tx:
      if IT.search(v):C[(t,v[:90])]+=1
  tot=sum(1 for _ in C)
  print(f'[{l}] frasi con parole italiane ancora visibili: {tot}')
  for (t,v),n in C.most_common(rep):print('   ',t,'|',v)
  r=await pg.evaluate("()=>({lang:document.documentElement.lang,menu:[...document.querySelectorAll('nav button')].slice(0,12).map(b=>b.textContent.trim()),pollo:fMatch('chicken breast').slice(0,3).map(f=>f.name),mela:fMatch('pomme').slice(0,2).map(f=>f.name),num:(1234.5).toLocaleString(LOC)})")
  print('  ',r)
  await pg.evaluate("()=>{V.tab='h';render()}");await pg.screenshot(path=gb.O+f'home-{l}.png',full_page=True)
  return pg,E,r,tot
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    rep=int(sys.argv[1]) if len(sys.argv)>1 else 40
    pe,Ee,re_,te=await lang(b,'en',rep)
    pf,Ef,rf,tf=await lang(b,'fr',rep)
    ok=lambda c,w:print(('ok  ' if c else 'FAIL ')+w)
    ok(re_['lang']=='en' and rf['lang']=='fr','attributo lang della pagina')
    ok(any('Pollo' in x for x in re_['pollo']),'ricerca «chicken breast» trova il pollo')
    ok(any('Mel' in x for x in rf['mela']),'ricerca «pomme» trova le mele')
    # cambio lingua dal menu: fr -> it
    await pf.evaluate("()=>document.body.classList.add('mo')");await pf.click('[data-a=lng][data-v=it]');await pf.wait_for_timeout(1500)
    ok(await pf.evaluate("()=>document.documentElement.lang")=='it','cambio lingua dal menu (FR → IT) con ricarica')
    ok(await pf.evaluate("()=>S.lang")=='it','lingua salvata nei dati (va nei backup)')
    ok(not Ee and not Ef,'nessun errore JS '+str(Ee+Ef))
    await b.close()
asyncio.run(m())
