import asyncio;from t import *
steps=["()=>{V.tab='s';V.pg={id:null,f:''};render();return 'tutti:'+document.querySelectorAll('.pgc').length}",
 "()=>{document.querySelector('[data-a=pgf][data-k=cl]').click();return 'a casa:'+[...document.querySelectorAll('.pgc b')].map(b=>b.textContent)}",
 "()=>{const r={};for(const k of ['23','4','56']){V.pg={id:null,f:k};render();r[k]=document.querySelectorAll('.pgc').length}return r}",
 "()=>{const out=[];for(const p of PGM.slice(8)){V.pg={id:null,f:''};render();document.querySelector('[data-a=pgo][data-k='+p[0]+']').click();const t1=document.querySelector('#v').textContent.length;document.querySelector('[data-a=pgu]').click();const n0=S.sch.length;document.querySelector('[data-a=pgok]').click();const n1=S.sch.length;const L=S.sch.slice(n0);out.push(p[0]+': schede '+(n1-n0)+' es '+L.map(x=>x.ex.length).join('/')+' ss '+L.map(x=>x.ss.length).join('/')+' giorni '+JSON.stringify(S.pl))}return out}",
 "()=>{V.pg={id:'phl',f:'',vi:0,step:1};render();return null}",("g1.png",)]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
