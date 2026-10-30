import asyncio;from t import *
steps=["()=>{V.tab='s';V.sd=null;V.ed='';render();return document.querySelectorAll('[data-a=sdm]').length}",
 "()=>{const n0=S.ex.length;document.querySelector('[data-a=sdm][data-v=\"0\"]').click();return {nuovi:S.ex.length-n0,nome:document.querySelector('#scn').value,es:document.querySelectorAll('.sdit').length,on:document.querySelector('[data-a=sdm].on').textContent}}",("k1.png",),
 "()=>{document.querySelector('[data-a=sdm][data-v=\"3\"]').click();return 'conferma:'+!document.querySelector('#cfm').hidden}",
 "()=>{document.querySelector('[data-a=sdmok]').click();const d=sdGet();return {nome:d.name,ex:d.ex.length,ss:d.ss.length,sup:!!document.querySelector('.sdss')}}",
 "()=>{document.querySelector('#scn').value='Upper mia';document.querySelector('[data-a=sca]').click();const x=S.sch.find(s=>s.name=='Upper mia');return x?{ex:x.ex.length,ss:x.ss.length,t:Object.values(x.t)[0],rt:Object.values(x.rt)[0]}:'NON SALVATA '+S.sch.map(s=>s.name)}",
 "()=>({tpl:sdGet().tpl||'nessuno',scn:document.querySelector('#scn').value})",
 "()=>{document.querySelector('[data-a=sdm][data-v=\"0\"]').click();return 'nome con duplicato? '+sdGet().name}",
 "()=>{const x=S.sch.find(s=>s.name=='Push-Pull A');V.ed=x.id;V.sd=null;render();return 'in modifica righe modelli: '+document.querySelectorAll('[data-a=sdm]').length}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
