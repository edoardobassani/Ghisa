# v219: Riepilogo Excel unico con ambiti a scelta (cruscotto, diario, progressi, calendario kcal, grafici); CSV per area
import asyncio,subprocess,time,os,json,zipfile,io
from playwright.async_api import async_playwright
import openpyxl
from lxml import etree
SRC=os.environ.get('SRC','/home/claude/w/tracker-palestra.html');W=os.path.dirname(SRC);O=W+'/u/';os.makedirs(O,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8787','--bind','127.0.0.1'],cwd=W,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
def check(path):
  z=zipfile.ZipFile(path);[etree.fromstring(z.read(n)) for n in z.namelist() if n.endswith(('.xml','.rels'))]
  wb=openpyxl.load_workbook(path);return [(ws.title,len(ws._charts)) for ws in wb.worksheets]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},accept_downloads=True);pg=await ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)))
    await pg.goto('http://127.0.0.1:8787/'+os.path.basename(SRC));await pg.wait_for_timeout(800)
    await pg.evaluate("async()=>{const d=await (await fetch('demo/demo_data.json')).json();Object.assign(S,d);S.wc=1;V.tab='x';V.xp='m3';render()}")
    async with pg.expect_download() as dl: await pg.click('[data-a=xmx]')
    f=await dl.value;pth=O+'v219-tutto.xlsx';await f.save_as(pth);print('file:',f.suggested_filename);print('tutti gli ambiti:',check(pth))
    for k in ['w','g','c']: await pg.click(f'[data-a=xesec][data-k={k}]')
    print('scelta:',await pg.evaluate("()=>JSON.stringify(V.xe)"))
    async with pg.expect_download() as dl: await pg.click('[data-a=xmx]')
    f=await dl.value;pth=O+'v219-dieta.xlsx';await f.save_as(pth);print('solo alimentazione:',check(pth))
    await pg.click('[data-a=xesec][data-k=n]');await pg.click('[data-a=xmx]');await pg.wait_for_timeout(200)
    print('nessun ambito:',await pg.evaluate("()=>$('#toast').textContent"))
    await pg.click('.xcsv summary')
    async with pg.expect_download() as dl: await pg.click('[data-a=xex][data-k=g]')
    f=await dl.value;t=open(await f.path(),encoding='utf-8-sig').read().splitlines();print('CSV palestra:',f.suggested_filename,t[0][:60],len(t))
    # periodo senza dati
    await pg.evaluate("()=>{V.xp='c';V.xa='2020-01-01';V.xb='2020-01-31';V.xe={g:1};render()}");await pg.click('[data-a=xmx]');await pg.wait_for_timeout(200)
    print('periodo vuoto:',await pg.evaluate("()=>$('#toast').textContent"))
    await pg.screenshot(path=O+'v219-ui.png',full_page=True)
    print('errori',E);await b.close()
asyncio.run(m());srv.terminate()
