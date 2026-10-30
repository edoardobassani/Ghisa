import asyncio;from t import *
c=lambda sel:f"()=>{{const b=document.querySelector({sel!r});if(!b)return 'MANCA '+{sel!r};b.click()}}"
steps=["()=>{V.tab='e';V.ek='p';V.o['ge_Petto']=1;render()}",("e1.png",),
 c('[data-a=exnt]'),("e2.png",),
 "()=>{document.querySelector('#exn2').value='Panca inclinata manubri';document.querySelector('#exnt2').value='panca a 30°'}",
 c('[data-a=exm][data-v=bw]'), "()=>document.querySelector('#exn2').value",
 c('[data-a=exm][data-v=\"\"]'),
 c('[data-a=exgp][data-v=Petto]'), c('[data-a=exok]'),
 "()=>JSON.stringify(S.ex.find(e=>e.name=='Panca inclinata manubri'))",
 # duplicato
 c('[data-a=exnt]'),"()=>{document.querySelector('#exn2').value='squat'}",c('[data-a=exok]'),"()=>'dialog aperto:'+!document.querySelector('#cfm').hidden",c('[data-a=exx]'),
 # gruppo nuovo
 c('[data-a=exnt]'),"()=>{document.querySelector('#exn2').value='Wrist curl'}",c('[data-a=exgo]'),"()=>{document.querySelector('#exgn').value='avambracci'}",c('[data-a=exm][data-v=bw]'),"()=>'gn conservato:'+document.querySelector('#exgn').value",c('[data-a=exok]'),
 "()=>JSON.stringify(S.ex.find(e=>e.name=='Wrist curl'))",
 # modifica con guida e cambio nome
 "()=>{const x=S.ex.find(e=>e.name=='Panca piana bilanciere');V.o['ge_Petto']=1;render();document.querySelector('[data-a=exe][data-i=\"'+x.id+'\"]').click();return document.querySelector('#exn2').value+'|'+document.querySelector('.cfb .hint:last-of-type').textContent}",("e3.png",),
 "()=>{document.querySelector('#exgd2').value='Posizione\\n- mia guida';document.querySelector('#exnt2').value='rack 5'}",c('[data-a=exok]'),
 "()=>{const x=S.ex.find(e=>e.name=='Panca piana bilanciere');return JSON.stringify({gd:x.gd,nt:x.nt,log:S.log.filter(l=>l.e==x.id).length})}",
 # elimina con conferma
 "()=>{const x=S.ex.find(e=>e.name=='Wrist curl');V.o['ge_Avambracci']=1;render();document.querySelector('[data-a=del][data-k=\"e:'+x.id+'\"]').click();return document.querySelector('[data-k=\"e:'+x.id+'\"]').textContent}",
 "()=>{const x=S.ex.find(e=>e.name=='Wrist curl');document.querySelector('[data-a=del][data-k=\"e:'+x.id+'\"]').click();return 'eliminato:'+!S.ex.some(e=>e.name=='Wrist curl')}",
 c('[data-a=seed]'),"()=>'catalogo:'+!!document.querySelector('#xbm:not([hidden]) #xbl')",
 "()=>{xbClose();V.o['ge_Petto']=1;render();window.scrollTo(0,0)}",("e4.png",),
 "()=>localStorage.getItem('ghisa').length>100"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
