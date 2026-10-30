import asyncio,json,re,time,sys
from playwright.async_api import async_playwright
from t import SEED
O='/home/claude/w/out5/'

GMOCK="""window.google={accounts:{oauth2:{initTokenClient(c){return{requestAccessToken(o){window.__auth=(window.__auth||0)+1;setTimeout(()=>c.callback({access_token:'tok'+window.__auth,expires_in:3600,scope:'https://www.googleapis.com/auth/drive.appdata email'}),50)}}},hasGrantedAllScopes(){return true},revoke(t,cb){cb&&cb()}}}};"""
F={};N=[0]
def lst():return [{'id':k,'name':v['name'],'modifiedTime':v['mt'],'size':str(len(v['c'])),'appProperties':v.get('ap',{})} for k,v in F.items()]
async def drive(route,req):
  u=req.url;m=req.method
  if 'userinfo' in u:return await route.fulfill(json={'email':'edo@example.com'})
  if '/upload/drive/v3/files' in u:
    ct=req.headers['content-type'];b=ct.split('boundary=')[1];parts=req.post_data_buffer.decode().split('--'+b)
    meta=json.loads(parts[1].split('\r\n\r\n',1)[1].rsplit('\r\n',1)[0]);body=parts[2].split('\r\n\r\n',1)[1].rsplit('\r\n',1)[0]
    mm=re.search(r'/files/([^?]+)\?',u)
    if m=='PATCH':fid=mm.group(1)
    else:N[0]+=1;fid='f%d'%N[0];F[fid]={'name':meta['name']}
    F[fid].update(c=body,mt=time.strftime('%Y-%m-%dT%H:%M:%SZ'));
    if 'appProperties' in meta:F[fid]['ap']=meta['appProperties']
    return await route.fulfill(json={'id':fid,'name':F[fid]['name']})
  mm=re.search(r'/drive/v3/files/([^?]+)',u)
  if mm and m=='DELETE':F.pop(mm.group(1),None);return await route.fulfill(status=204,body='')
  if mm and 'alt=media' in u:return await route.fulfill(body=F[mm.group(1)]['c'],content_type='application/json')
  if '/drive/v3/files' in u:return await route.fulfill(json={'files':lst()})
  await route.fulfill(status=404,body='')
async def page(b,dev):
  ua='Mozilla/5.0 (Linux; Android 14) Mobile' if dev=='tel' else 'Mozilla/5.0 (X11; Linux x86_64)'
  ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,user_agent=ua);pg=await ctx.new_page()
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.add_init_script(GMOCK);await pg.route(re.compile(r'https://www\.googleapis\.com/.*'),drive)
  await pg.goto('file:///home/claude/w/tracker-palestra.html');await pg.wait_for_timeout(400);return pg,errs
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    pg,e1=await page(b,'tel')
    await pg.evaluate(SEED);await pg.evaluate("()=>{pPut({id:'ph1',d:today(),a:'Fronte',u:'data:image/jpeg;base64,AAAA'})}");await pg.reload();await pg.wait_for_timeout(600)
    await pg.evaluate("()=>document.body.classList.add('mo')");await pg.wait_for_timeout(300);await pg.evaluate("()=>document.querySelector('#nbk').scrollIntoView()");await pg.wait_for_timeout(200);await pg.screenshot(path=O+'1-menu-off.png')
    await pg.click('#nbk [data-a=dvsh]');await pg.wait_for_timeout(400);await pg.screenshot(path=O+'0-guida.png')
    await pg.fill('#dvcid','12345-abc.apps.googleusercontent.com');await pg.click('[data-a=dvck]');await pg.wait_for_timeout(300);print('cid',await pg.evaluate("()=>DVS.cid"))
    await pg.click('#cfm [data-a=dvcon]');await pg.wait_for_timeout(1500);await pg.evaluate("()=>cfClose()")
    print('collegato',await pg.evaluate("()=>[DVS.on,DVS.em,!!DVS.last,dvDirty()]"),sorted(v['name'] for v in F.values()))
    await pg.evaluate("()=>document.body.classList.add('mo')");await pg.wait_for_timeout(300);await pg.evaluate("()=>document.querySelector('#nbk').scrollIntoView()");await pg.wait_for_timeout(200);await pg.screenshot(path=O+'2-menu-on.png')
    # modifica -> salvataggio automatico dopo 5 s
    await pg.evaluate("()=>{document.body.classList.remove('mo');S.wt.push({d:today(),kg:80});save()}");await pg.wait_for_timeout(6500)
    d=[v for v in F.values() if v['name'].startswith('d-')][0];print('auto',json.loads(d['c'])['data']['wt'][-1],await pg.evaluate("()=>dvDirty()"))
    await pg.evaluate("()=>document.body.classList.add('mo')");await pg.wait_for_timeout(200);await pg.click('[data-a=dvsh]');await pg.wait_for_timeout(800);await pg.screenshot(path=O+'3-foglio.png')
    # foto cancellata -> rimossa da Drive
    await pg.evaluate("()=>pDel('ph1').then(loadPh)");await pg.wait_for_timeout(6000);print('foto',sorted(v['name'] for v in F.values()))
    # token scaduto -> barra in Home
    await pg.evaluate("()=>{cfClose();DRV.tk='';DRV.exp=0;DVS.last=Date.now()-3*864e5;dvKeep();S.wt.push({d:today(),kg:79});save();V.tab='h';render()}");await pg.wait_for_timeout(300);await pg.screenshot(path=O+'4-home-bar.png')
    await pg.click('#dvbar [data-a=dvnow]');await pg.wait_for_timeout(1200);print('dopo tocco',await pg.evaluate("()=>[dvOk(),dvDirty(),!!document.querySelector('#dvbar:not([hidden])')]"))
    # secondo dispositivo: computer con dati vecchi
    pc,e2=await page(b,'pc');await pc.evaluate(SEED);await pc.evaluate("()=>{S.svd=Date.now()-864e5;S.wt=[];dPut('S',S)}");await pc.reload();await pc.wait_for_timeout(600)
    await pc.evaluate("()=>{S.svd=Date.now()-864e5}")
    await pc.evaluate("()=>document.body.classList.add('mo')");await pc.wait_for_timeout(200);await pc.evaluate("()=>{DVS.cid='12345-abc.apps.googleusercontent.com';render()}");await pc.click('#nbk [data-a=dvcon]');await pc.wait_for_timeout(1500);await pc.screenshot(path=O+'5-conflitto.png')
    await pc.click('[data-a=dvuse]');await pc.wait_for_timeout(1500);print('pc ripristinato',await pc.evaluate("()=>[S.wt.length,PH.length]"))
    print('copia prima',await pc.evaluate("()=>dGet('prev').then(x=>!!(x&&x.S))"))
    print('errs',e1,e2);await b.close()
asyncio.run(main())
