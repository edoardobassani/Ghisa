import asyncio;from t import *
Q=['petto pollo','pollo petto','pomodoro','pomodori','uovo','mele','mela','caffe','latte parzialmente','riso basmati','basmati riso','pane','yogurt greco','parmigiano','tonno','olio','passata pomodoro','prosciutto cotto','fiocchi avena','pol','zzz']
steps=["(Q)=>0","()=>{const Q="+str(Q)+";return Q.map(q=>{const L=fMatch(q)||[];return q+' -> '+L.length+': '+L.slice(0,3).map(f=>f.name).join(' | ')}).join('\\n')}",
 "()=>{const a=performance.now();for(let i=0;i<20;i++)fMatch('petto pollo');return 'ms per ricerca: '+((performance.now()-a)/20).toFixed(1)}",
 "()=>{V.tab='n';V.fsh='Pranzo';V.fq='';render();const q=document.querySelector('#fq');q.value='pomodori';q.dispatchEvent(new Event('input',{bubbles:true}));return document.querySelector('#fl').innerText.slice(0,200)}",("s19.png",),
 "()=>{const b=document.querySelector('[data-a=fqall]');if(b){b.click();return 'tutti:'+document.querySelectorAll('#fl .fr').length}return 'nessun pulsante'}",
 "()=>{document.querySelector('#fl [data-a=fsel]').click();return 'grammi:'+!!document.querySelector('.fgi')}",
 "()=>{const q=document.querySelector('#fq');q.value='zzz';q.dispatchEvent(new Event('input',{bubbles:true}));return document.querySelector('#fl').innerText}",
 "()=>{gsearch('petto pollo');return document.querySelector('#gsr').textContent.slice(0,150)}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
