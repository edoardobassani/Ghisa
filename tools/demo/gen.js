()=>{
let seed=20261030;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648};const ri=(a,b)=>a+Math.floor(rnd()*(b-a+1));const pick=a=>a[Math.floor(rnd()*a.length)];const r25=v=>Math.round(v/2.5)*2.5;
const D0='2025-10-31',D1='2026-10-29';const days=[];for(let d=D0;d<=D1;d=hvAdd(d,1))days.push(d);
const wd=d=>(new Date(d+'T12:00:00').getDay()+6)%7;
try{localStorage.clear()}catch(e){};norm({ex:[],sch:[],log:[]});S.ses=[];S.gv=2;
S.pf={sx:'m',age:35,act:1.55};S.h=178;S.rest=90;S.gw=4;S.gc=2;S.dlw=5;
// --- programmi: PPL poi Upper/Lower
function mk(pid,start){V.pg={id:pid,f:'',vi:0,step:2,keep:false,days:[],pl:PGM.find(x=>x[0]==pid)[8][0][1].slice()};pgDo();S.prog.start=start;return S.prog.ids.slice()}
const PPL=mk('ppl','2025-10-31'),UL=mk('ul4','2026-03-02');
// --- stato carichi
const st={};const base={'Panca piana bilanciere':62.5,'Panca inclinata manubri':20,'Military press':37.5,'Alzate laterali':8,'Croci ai cavi':12.5,'Push down corda':22.5,'Stacco da terra':100,'Rematore bilanciere':55,'Face pull':17.5,'Curl bilanciere':25,'Curl martello':12,'Squat':80,'Leg press':140,'Stacco rumeno':70,'Leg curl sdraiato':35,'Calf raise in piedi':60,'Lat machine':50,'Pulley basso':50,'Leg extension':45,'Leg curl seduto':35,'Affondi':16,'Hip thrust':80,'Curl manubri':12,'French press':25,'Panca inclinata bilanciere':55,'Rematore manubrio':26,'Lento avanti manubri':18,'Calf raise seduto':40,'Front squat':60,'Croci con manubri':12,'Crunch ai cavi':30,'Face pull ':17.5};
const exS=id=>{const e=S.ex.find(x=>x.id==id);return e};
function stOf(id){if(st[id])return st[id];const e=exS(id);const b=base[e.name];st[id]={kg:b!=null?b:(isBW(id)?0:20),ok:0,stall:0,rep:0};st[id].b0=st[id].kg||1;return st[id]}
const NOTES=['ottime sensazioni','tecnica pulita','pausa lunga, stanco','ultima serie al cedimento','spalla un po’ rigida','presa larga','dormito poco'];
let ses=0,dl=0;
const off=d=>(d>='2025-12-22'&&d<='2026-01-04')||(d>='2026-08-08'&&d<='2026-08-23')||(d>='2026-04-04'&&d<='2026-04-06');
days.forEach((d,k)=>{if(d>='2026-08-31')return;const w=wd(d),prog=d<'2026-03-02'?PPL:UL,pl=d<'2026-03-02'?[0,-1,1,-1,2,-1,-1]:[0,1,-1,2,3,-1,-1];
 let j=pl[w];if(off(d)&&rnd()<.85)j=-1;
 if(j>=0&&rnd()<.12)j=-1; // saltata
 const wk=Math.floor(k/7),deload=wk%6==5;
 if(j>=0){const sc=S.sch.find(x=>x.id==prog[j]);const sid='ss'+(++ses);const t0=new Date(d+'T'+pad(ri(17,19))+':'+pad(ri(0,59))+':00').getTime();let n=0;
  const cut=d<'2026-05-10';
  sc.ex.forEach(id=>{const T=sc.t[id]||{s:3,r:10},s=stOf(id),bw=isBW(id),sets=deload?Math.ceil(T.s/2):T.s,tr=T.r=='max'?0:+T.r;const ok=deload||rnd()<(cut?.58:.7);
   for(let i=0;i<sets;i++){let r;if(bw){r=T.r=='max'?Math.max(3,Math.round(6+s.rep*.08)+ri(-1,1)-i):tr+ri(-2,0);}else{r=ok?tr+(i==0&&rnd()<.4?1:0):Math.max(1,tr-(i>=sets-2?ri(1,2):0))}
    const L={id:uid()+i,d,e:id,kg:bw?0:s.kg,r,ss:sid};if(rnd()<.3)L.rir=ok?ri(1,3):ri(0,1);if(rnd()<.04)L.n=pick(NOTES);S.log.push(L);n++}
   s.rep++;if(!bw&&!deload){if(ok){s.stall=0;if(rnd()<(s.kg<20?.3:.42)*Math.max(.04,1-(s.kg/s.b0-1)*3.2)){const inc=s.kg<20?1:s.kg<60?2.5:2.5;s.kg=Math.round((s.kg+inc)*10)/10}}else{s.stall++;if(s.stall>=5){s.kg=r25(s.kg*.92)||s.kg;s.stall=0}}}});
  const dur=ri(48,78);S.ses.push({id:sid,d,sc:sc.id,t0,t1:t0+dur*60000,n});}
});
// --- cardio
days.forEach(d=>{const w=wd(d);if(off(d)&&rnd()<.6)return;if(d>='2026-09-07'&&w!=6)return;let t=null,min=0,km=0;
 if(w==6&&rnd()<.75){t='Camminata';min=ri(45,80);km=Math.round(min/60*5.2*10)/10}
 else if((w==1||w==3)&&rnd()<.55){t=pick(['Corsa','Corsa','Cyclette','Ellittica']);min=t=='Corsa'?ri(25,40):ri(20,35);km=t=='Corsa'?Math.round(min/60*(9.5+rnd()*1.8)*10)/10:t=='Cyclette'?Math.round(min/60*24*10)/10:0}
 else if(w==5&&rnd()<.25){t='Bici';min=ri(60,110);km=Math.round(min/60*22*10)/10}
 if(!t)return;const o={id:uid(),d,t,min};if(km)o.km=km;const e=cdEst(t,min,km,d);if(e){o.kc=e;o.est=1}S.cd.push(o)});
// --- peso e misure
const wAt=d=>{const a=Date.parse(d),t=(a-Date.parse(D0))/864e5;return t<190?85-6*t/190:79+1.4*Math.min(1,(t-190)/170)};
days.forEach(d=>{if(rnd()<.7){const kg=Math.round((wAt(d)+(rnd()-.5)*1.1+(wd(d)==0?.4:0))*10)/10;S.wt.push({id:uid(),d,kg})}});
for(let k=0;k<days.length;k+=28){const d=days[k],f=(85-wAt(d))/6;S.ms.push({id:uid(),d,v:{collo:Math.round((39.5-.6*f)*10)/10,petto:Math.round((104-2*f+(k>200?1:0))*10)/10,vita:Math.round((94-7*f+rnd()*.6)*10)/10,fianchi:Math.round((102-3.5*f)*10)/10,braccio:Math.round((35+.4*k/364)*10)/10,coscia:Math.round((58-1.2*f)*10)/10,polpaccio:Math.round(38.5*10)/10}})}
// --- dieta
const FF={};const F=q=>{if(FF[q])return FF[q];const A=allF(),ql=q.toLowerCase(),f=A.find(x=>x.name.toLowerCase()==ql)||A.find(x=>x.name.toLowerCase().startsWith(ql))||A.find(x=>x.name.toLowerCase().includes(ql));if(!f)throw new Error('alimento mancante: '+q);return FF[q]=f.id};
const MEALS={Colazione:[[['latte di vacca, uht, parzialmente',200,250],['fette biscottate',30,40],['marmellata',20,25]],[['yogurt greco 0%',170,170],['fiocchi d',40,60],['banana',100,130]],[['caffè (senza',30,30],['pane integrale',50,70],['miele',15,20]]],
 Pranzo:[[['pasta di semola (cruda)',80,100],['passata di pomodoro',100,150],['olio extra',10,12],['parmigiano reggiano',10,15]],[['riso basmati, crudo',80,90],['petto di pollo (crudo)',150,180],['zucchine',150,250],['olio extra',10,10]],[['pane integrale',80,100],['bresaola',60,80],['lattuga',80,120],['olio extra',10,10]],[['farro (crudo)',80,90],['tonno al naturale',80,80],['pomodori',150,200],['olio extra',10,10]]],
 Cena:[[['salmone',150,180],['patate',200,300],['olio extra',10,10],['lattuga',80,100]],[['uova di gallina, intero, cotto, alla coque',110,165],['pane integrale',50,70],['spinaci',200,250],['olio extra',10,10]],[['merluzzo',180,220],['pane integrale',50,70],['finocchi',150,200],['olio extra',10,10]],[['manzo magro',150,170],['patate',200,250],['carote',150,150],['olio extra',10,10]]],
 Spuntino:[[['mela',150,180]],[['mandorle',20,30]],[['yogurt greco 0%',125,170]],[['banana',110,130]]]};
const PZ0=[['pizza margherita',300,330]];
days.forEach(d=>{if(rnd()<.14&&d<'2026-10-25')return;const w=wd(d),cut=d<'2026-05-10';MP.forEach(m=>{if(m=='Spuntino'&&rnd()<.35)return;if(m=='Colazione'&&rnd()<.05)return;let T=pick(MEALS[m]);if(m=='Cena'&&w==5&&rnd()<.6)T=PZ0;const sc=cut?.92:1.08;T.forEach(([q,a,b])=>S.meal.push({id:uid(),d,m,f:F(q),g:Math.round(ri(a,b)*(q.includes('olio')?1:sc))}))})});
{const by={};S.meal.forEach(m=>(by[m.d]=by[m.d]||[]).push(m));Object.entries(by).forEach(([d,L])=>{const tg=(d<'2026-05-10'?2150:2600)*(0.9+rnd()*0.22)+(wd(d)==5?250:0),k=L.reduce((t,m)=>t+ln(m).k,0);if(!k)return;const f=Math.max(.8,Math.min(2.2,tg/k));L.forEach(m=>{const n=(fo(m.f)||{}).name||'';if(!/olio/i.test(n))m.g=Math.round(m.g*f/5)*5||m.g})})}
{const t=today();[['latte di vacca, uht, parzialmente',250],['fette biscottate',40],['marmellata',25]].forEach(([q,g])=>S.meal.push({id:uid(),d:t,m:'Colazione',f:F(q),g}));S.wt.push({id:uid(),d:t,kg:80.1})}
S.goal=2450;S.gm={p:150,c:0,f:0};
S.sm=[{id:uid(),name:'Colazione classica',items:[{f:F('latte di vacca, uht, parzialmente'),g:250},{f:F('fette biscottate'),g:35},{f:F('marmellata'),g:20}],u:40},{id:uid(),name:'Pollo e riso',items:[{f:F('riso basmati, crudo'),g:85},{f:F('petto di pollo (crudo)'),g:170},{f:F('zucchine'),g:200},{f:F('olio extra'),g:10}],u:25}];

// --- da settembre: programma di forza a blocchi (Forza lineare 12 sett.), lun/mer/ven
S.tmp=90;
{const p=bpStart(bpRes(bpmLin()),[0,2,4]);const d0='2026-08-31';
 const doSes=(j,d)=>{const sc=S.sch.find(x=>x.id==p.sch[j]),sid='ss'+(++ses),t0=new Date(d+'T'+pad(ri(17,19))+':'+pad(ri(0,59))+':00').getTime();let n=0;
  sc.ex.forEach(id=>{const T=sc.t[id],s=stOf(id);(T.sets||[]).forEach((x,i)=>{const kg=x.kg||s.kg,am=x.r=='max',r=am?ri(4,8):Math.max(1,+x.r-(rnd()<.08?1:0));const L={id:uid()+i,d,e:id,kg,r,ss:sid,...(am?{f:1}:{})};if(rnd()<.3)L.rir=am?0:ri(1,3);S.log.push(L);n++});if(T.sets&&T.sets[0]&&T.sets[0].kg)s.kg=T.sets[0].kg});
  S.ses.push({id:sid,d,sc:sc.id,t0,t1:t0+ri(55,75)*60000,n});return t0};
 for(let k=0;k<9;k++){const ws=Date.parse(hvAdd(d0,7*k)+'T00:00:00');p.ws=ws;const L=k<8?[0,1,2]:[0,1];L.forEach(j=>doSes(j,hvAdd(d0,7*k+2*j)));if(k<8){bpNext(1);p.ws=Date.parse(hvAdd(d0,7*(k+1))+'T00:00:00')}}
 const sq=S.ex.find(e=>e.name=='Stacco da terra');S.rm={[sq.id]:{kg:170,src:'t',d:'2026-09-05',h:[{d:'2026-09-05',kg:170,src:'t'}]}}}
// --- cardio da settembre: programma a blocchi «Fondo e VO2max» (mar/gio) e uscite importate dall'orologio
{const p=CPM.find(x=>x[0]=='vo2');S.cpr={id:'vo2',days:[1,3,6],t:'Cyclette',pos:0,start:'2026-09-08',last:''};S.gc=3;
 days.filter(d=>d>='2026-09-08'&&[1,3].includes(wd(d))).forEach(d=>{if(rnd()<.1)return;const sp=cpSes(p,S.cpr.pos),min=cpMin(sp),o={id:uid(),d,t:'Cyclette',min,cp:'vo2',rt:pick(['g','g','f','d'])};const e=cdEst('Cyclette',min,0,d);if(e){o.kc=e;o.est=1}S.cd.push(o);if(o.rt!='d')S.cpr.pos++;S.cpr.last=d});}
// percorsi GPX (domenica) con battito, e due sessioni registrate dal vivo
{const route=(n,R,amp,t0,secPt)=>{const P=[];for(let i=0;i<=n;i++){const a=i/n*2*Math.PI,r=R*(1+.18*Math.sin(3*a));P.push({lat:45.4642+r*Math.sin(a)/111000,lon:9.19+r*Math.cos(a)/(111000*.7),e:120+amp*Math.sin(2*a)+6*Math.sin(5*a),t:t0+i*secPt*1000,hr:Math.round(105+20*Math.min(1,i/(n*.15))+(rnd()-.5)*6)})}return P};
 days.filter(d=>d>='2026-09-06'&&wd(d)==6).forEach((d,k)=>{if(rnd()<.15)return;const run=k%2==1,t0=new Date(d+'T09:'+pad(ri(0,40))+':00').getTime(),P=route(240,run?1100:900,run?25:15,t0,run?7.5:12).map(x=>({...x,hr:run?x.hr+30:x.hr}));
  const a=gxStats({nm:'',ty:run?'Corsa':'Camminata',P,src:'Huawei Health'});a.sel=a.ty;a.d=d;const K=gxKc(a);const o={id:uid(),d,t:a.sel,min:Math.round(a.mv/60*10)/10,km:a.km,src:'file',from:'Huawei Health',st:a.st,el:a.el,asc:a.asc,elv:a.elv,hr:a.hr,rte:a.rt,sp:a.sp};if(K.kc){o.kc=K.kc;if(K.s=='met')o.est=1}S.cd=S.cd.filter(c=>!(c.d==d&&c.t=='Camminata'&&!c.src));S.cd.push(o)});
 ['2026-10-17','2026-10-24'].forEach(d=>{const t0=new Date(d+'T10:15:00').getTime(),N=35*60;const hs=[],hz=[0,0,0,0,0];for(let i=0;i<240;i++){const b=Math.round(100+52*Math.min(1,i/30)+(i>150&&i<190?10:0)+(rnd()-.5)*5);hs.push(b);const z=hrZ(b);if(z>=0)hz[z]+=N/240/60}
  const a=Math.round(hs.reduce((x,y)=>x+y,0)/hs.length),o={id:uid(),d,t:'Corsa',min:35,km:5.6,src:'live',st:t0,el:N+120,hr:{a,m:Math.max(...hs)},hs,hz:hz.map(x=>Math.round(x*10)/10)};o.kc=hrKcal(a,35,d);S.cd.push(o)})}
S.cd.sort((a,b)=>a.d<b.d?-1:1);
S.lb=hvAdd(D1,-3);S.bks=hvAdd(D1,-3);
save();
return {bp:S.bp&&[S.bp.n,S.bp.wk],cpr:S.cpr&&S.cpr.pos,ex:S.ex.length,sch:S.sch.length,log:S.log.length,ses:S.ses.length,cd:S.cd.length,meal:S.meal.length,wt:S.wt.length,ms:S.ms.length,last:S.wt.slice(-1)[0].kg,panca:st[S.ex.find(e=>e.name=='Panca piana bilanciere').id].kg,squat:st[S.ex.find(e=>e.name=='Squat').id].kg}}
