import asyncio;from t import *
steps=["()=>{const c={};allF().forEach(f=>{const g=cat(f);c[g]=(c[g]||0)+1});return JSON.stringify(c)}",
 "()=>['Petto di pollo (crudo)','Patate','Melanzane','Babaco, fresco','Tofu','Pasta all’uovo (cruda)','Pasta alla carbonara','Fiocchi d’avena','Proteine whey (polvere)','Olio extravergine d’oliva','Yogurt greco 0%','Soia, isolato proteico'].map(n=>n+' → '+cat(allF().find(f=>f.name==n))).join('\\n')",
 "()=>{S.food.push({id:'u1',name:'Pancake proteici',k:220,p:20,c:25,f:4},{id:'u2',name:'Broccoli al vapore',k:30,p:3,c:4,f:0.4,cg:'Verdure'},{id:'u3',name:'Mix',k:100,p:1,c:1,f:1,cg:'Proteine'});CATC=new Map();return ['u1','u2','u3'].map(i=>cat(fo(i))).join(', ')}",
 "()=>{V.tab='n';V.fsh='Pranzo';V.fq='';render();return [...document.querySelectorAll('#fl summary')].map(x=>x.textContent).join(' | ')}",("g20.png",),
 "()=>{V.fsh='';V.o.dNf=true;render();return [...document.querySelectorAll('#fcg option')].length}",
 "()=>{V.tab='pp';render();return 'piano pasti ok'}"]
r,e=asyncio.run(run(steps));print('\n'.join(map(str,r)));print('ERR',e)
