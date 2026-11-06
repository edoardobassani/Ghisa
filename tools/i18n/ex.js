const acorn=require('/opt/npm-tools/node_modules/acorn'),walk=require('/opt/npm-tools/node_modules/acorn-walk'),fs=require('fs');
const src=fs.readFileSync('app.js','utf8');const ast=acorn.parse(src,{ecmaVersion:2022,sourceType:'script'});
const segs=new Map(),add=(t,k)=>{t=t.replace(/\s+/g,' ').trim();if(!t)return;if(!/[A-Za-zÀ-ÿ]{2}/.test(t))return;const o=segs.get(t)||{n:0,k};o.n++;segs.set(t,o)};
const P='\u0001';
function proc(T,kind){ // T: testo con segnaposto \u0001
  if(T.length>3000&&/\|/.test(T))return; // dati
  // attributi
  T.replace(/\b(placeholder|aria-label|title|alt)="([^"]*)"/g,(m,a,v)=>{add(v,'attr');return m});
  const hasTag=/<[a-zA-Z\/!]/.test(T);
  if(hasTag){T.replace(/<[^>]*>/g,'\u0002').split('\u0002').forEach(x=>add(x,'html'))}
  else add(T,kind)}
walk.full(ast,n=>{
  if(n.type=='Literal'&&typeof n.value=='string')proc(n.value,'str');
  else if(n.type=='TemplateLiteral'){let T='';n.quasis.forEach((q,i)=>{T+=q.value.cooked;if(i<n.expressions.length)T+=P});proc(T,'tpl')}});
const out=[...segs].map(([t,o])=>({t,n:o.n,k:o.k}));
fs.writeFileSync('segs.json',JSON.stringify(out,null,0));
console.log(out.length);
