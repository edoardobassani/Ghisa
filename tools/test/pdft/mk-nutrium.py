import sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob
f=[x for x in glob.glob('/usr/share/fonts/**/DejaVuSans.ttf',recursive=True)][0]
pdfmetrics.registerFont(TTFont('DV',f))
P=[('07:00','COLAZIONE',[None,["5 fette biscottate","70 grammi di pane comune","50 grammi di cereali","50 grammi di fiocchi di avena","3 Pancakes (secondo la tua ricetta di cui ti mando i valori nutrizionali in allegato)"],["1 vasetto di yogurt greco da 150g","50 grammi di formaggio fresco spalmabile","50 grammi di hummus di","50 grammi di affettato magro o salmone affumicato (saltuariamente)","2 uova","70 grammi di fiocchi di latte magro"],["10 grammi di frutta secca o crema di frutta secca"]]),
 ('10:00','SPUNTINO DI METÀ MATTINA',[None,["1 porzione di frutta"],["20 grammi di frutta, secca"],["1 pacchetto di crackers"]]),
 ('13:00','PRANZO',['ANTIPASTO',["10 grammi di olio di oliva extravergine"],["1 porzione di verdura (almeno 150g)"],'PRIMO PIATTO',["120 grammi di pasta","120 grammi di riso","120 grammi di quinoa","120 grammi di farro","250 grammi di gnocchi di patate","400 grammi di patate"],'SECONDO PIATTO',["200 grammi di legumi (in media), cotti","4 uova (anche sotto forma di frittata)","1 scatoletta media di tonno al naturale","250 grammi di carne bianca o pesce magro","180 grammi di ricotta o altro formaggio fresco","220 grammi di tofu","180 grammi di seitan","150 grammi di tempeh"]]),
 ('16:00','MERENDA',[None,["1 porzione di frutta"],["1 vasetto di yogurt greco 0%","50 grammi di prosciutto cotto o altro affettato magro (saltuariamente)"],["1 porzione di pane integrale (50 g)","35 grammi di cereali"]]),
 ('20:00','CENA',['ANTIPASTO',["1 porzione di verdura (almeno 150g)"],["20 grammi di olio di oliva extravergine"],'PRIMO PIATTO',["150 grammi di pane","400 grammi di patate","100 grammi di pasta","100 grammi di riso","100 grammi di quinoa","100 grammi di farro","200 grammi di gnocchi freschi"],'SECONDO PIATTO',["4 uova","2 scatolette medie di tonno al naturale","220 grammi di seitan","200 grammi di tempeh","250 grammi di ricotta o altro formaggio fresco","350 grammi di carne bianca o pesce magro"]])]
def mk(out,mode):
  c=canvas.Canvas(out,pagesize=(595,842));y=[800]
  def t(x,s,sz=9,font='DV'):
    c.setFont(font,sz);c.drawString(x,y[0],s)
  def nl(d=14):
    y[0]-=d
    if y[0]<60:c.showPage();y[0]=800
  t(45,'nutrium',16);t(250,'Alessandro Magro');t(400,'+39 351 000 0000');nl(30)
  t(45,'INFORMAZIONI SUL CLIENTE',10);nl(18);t(95,'Edoardo Bassani');t(250,'ETÀ 27 anni');t(400,'ALTEZZA 180.0 cm');nl(14);t(400,'PESO 93.0 kg');nl(30)
  t(45,'PASTI',11);nl(24)
  for tm,meal,blocks in P:
    t(45,tm,9);t(75,meal,9);nl(15)
    for b in blocks:
      if b is None:continue
      if isinstance(b,str):t(75,b);nl(15);continue
      sep={'circ':' ○ ','o':' o ','gap':' § '}[mode]
      txt=sep.join(b);words=txt.split(' ');line='';first=True
      def out_line(L,first):
        if first:c.setFont('DV',9);c.drawString(78,y[0],'•')
        if '§' not in L:t(88,L);return
        x=88;parts=L.split('§')
        for k,pc in enumerate(parts):
          pc=pc.strip()
          if pc:c.setFont('DV',9);c.drawString(x,y[0],pc);x+=pdfmetrics.stringWidth(pc,'DV',9)
          if k<len(parts)-1:c.circle(x+7,y[0]+3,2.2,stroke=1,fill=0);x+=14
      for w in words:
        if len(line)+len(w)>95:
          out_line(line.strip(),first);first=False;nl(13);line=''
        line+=w+' '
      out_line(line.strip(),first);nl(15)
    nl(6)
  nl(20);t(400,'(Alessandro Magro)');c.showPage();y[0]=800
  t(45,'RICETTE',11);nl(20);t(45,'PANCAKE EDOARDO',12);t(400,'80 Pancakes');nl(30)
  t(45,'INGREDIENTI',11);nl(18);t(55,'• 2000 grammi di uovo di gallina, albume');nl(14);t(55,'• 1000 grammi di farina di frumento, tipo 00');nl(26)
  t(45,'INFORMAZIONI NUTRIZIONALI',11);nl(18);
  for r in [('','PER 100 g','PER PANCAKE (50 g)'),('ENERGIA','120 kcal','60 kcal'),('PROTEINE','10 g','5 g'),('CARBOIDRATI','20 g','10 g'),('LIPIDI','0 g','0 g')]:
    t(50,r[0]);t(160,r[1]);t(260,r[2]);nl(16)
  c.save()
for m in ['circ','o','gap']:mk(f'nutrium_{m}.pdf',m)
