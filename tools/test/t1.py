import asyncio;from t import *
steps=["()=>{V.tab='e';V.ek='p';V.o.dEl=1;V.o['ge_Petto']=1;render()}",
"()=>{const p=S.ex.find(e=>e.name=='Panca piana bilanciere').id;document.getElementById('gdx_'+p).querySelector('summary').click();return 'aperta:'+!!document.querySelector('#gdx_'+p+'[open] h4')}",
("s1.png",),
"()=>{const b=document.querySelector('.gdl [data-a=gde][data-i=myx]');b.click();return 'edit:'+!!document.querySelector('#gdt')}",
"()=>{document.querySelector('#gdt').value='Posizione\\n- prova';document.querySelector('[data-a=gds]').click();return 'salvata:'+(S.ex.find(e=>e.id=='myx').gd)}",
"()=>({gdl:document.querySelectorAll('.gdl').length,ex:S.ex.length})"]
print(asyncio.run(run(steps)))
