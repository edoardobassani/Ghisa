#!/usr/bin/env python3
"""Genera un anno di dati simulati con le funzioni dell'app (gen.js) e costruisce la pagina demo.
Uso: python3 tools/demo/make-demo.py [--rigenera]   (SRC=sorgente, predefinito /home/claude/w/tracker-palestra.html)
Senza --rigenera riusa demo_data.json. La pagina esce in ghisa-demo.html accanto a questo file.
La demo non si avvia né si aggiorna se non lo chiede Edo."""
import asyncio,os,sys
D=os.path.dirname(os.path.abspath(__file__));SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html')
async def gen():
  from playwright.async_api import async_playwright
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page();e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    await pg.goto('file://'+SRC);await pg.wait_for_timeout(800)
    print(await pg.evaluate(open(os.path.join(D,'gen.js')).read()))
    await pg.wait_for_timeout(300)
    d=await pg.evaluate("()=>JSON.stringify(S)");open(os.path.join(D,'demo_data.json'),'w').write(d);print('errori:',e);await b.close()
if '--rigenera' in sys.argv:asyncio.run(gen())
s=open(SRC).read();d=open(os.path.join(D,'demo_data.json')).read()
def R(a,b):
  global s;c=s.count(a);assert c==1,(c,a[:80]);s=s.replace(a,b)
R("<title>Ghisa – tracker palestra</title>","<title>Ghisa – demo un anno</title>")
R("let S=null;\ntry{S=JSON.parse(localStorage.getItem('ghisa'))}catch(e){}","const DEMO="+d.replace('</','<\\/')+";\nlet S=null;\nS=JSON.parse(JSON.stringify(DEMO));")
# demo: niente salvataggio e avvio immediato con i dati incorporati
R("function dataBoot(){return new Promise(done=>{","function dataBoot(){DBM='demo';BOOTED=true;return Promise.resolve();return new Promise(done=>{")
R("let SV=0;const save=()=>{if(window.__wiped)return;","let SV=0;const save=()=>{return true;if(window.__wiped)return;")
R("#prt{display:none}","#prt{display:none}\n#demo{position:fixed;top:calc(15px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);z-index:21;background:var(--hi);color:#1c262b;font:600 11.5px Barlow,sans-serif;padding:4px 10px;border-radius:10px;white-space:nowrap;pointer-events:none}body.ssm #demo,body.mo #demo{display:none}")
i=s.index('<body');j=s.index('>',i)+1
s=s[:j]+'\n<div id="demo">DEMO · un anno simulato · non si salva</div>'+s[j:]
open(os.path.join(D,'ghisa-demo.html'),'w').write(s);print('Demo scritta:',os.path.join(D,'ghisa-demo.html'),len(s),'byte')
