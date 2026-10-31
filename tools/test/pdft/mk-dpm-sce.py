V=['Zucchine','Spinaci','Peperoni','Carote','Broccoli','Fagiolini','Pomodori']
VC=['Lattuga','Fagiolini','Pomodori','Zucchine','Broccoli','Finocchi','Spinaci']
COL=["Fette biscottate:45,Yogurt greco 0%:150,Mandorle:10","Fiocchi d’avena:50,Yogurt greco 0%:150,Noci:10","Pane bianco:70,Formaggio spalmabile:50,Mandorle:10","Pancake:120,Yogurt greco 0%:150,Noci:10","Pane bianco:70,Bresaola:50,Mandorle:10","Fette biscottate:45,Uovo intero:100,Noci:10","Fiocchi d’avena:50,Fiocchi di latte:70,Mandorle:10"]
PR=[("Pasta di semola (cruda):120","Lenticchie lesse:200"),("Riso (crudo):120","Uovo intero:200"),("Quinoa (cruda):120","Petto di pollo (crudo):250"),("Farro (crudo):120","Ricotta vaccina:180"),("Gnocchi di patate:250","Merluzzo:250"),("Patate:400","Tofu:220"),("Pasta di semola (cruda):120","Ceci in scatola:200")]
CE=[("Pane bianco:150","Uovo intero:200"),("Patate:400","Petto di pollo (crudo):350"),("Pasta di semola (cruda):100","Tonno al naturale:120"),("Riso (crudo):100","Merluzzo:350"),("Quinoa (cruda):100","Seitan:220"),("Farro (crudo):100","Ricotta vaccina:250"),("Gnocchi di patate:200","Tempeh:200")]
F=['Mela','Kiwi','Banana','Arancia','Pera','Mela','Kiwi'];F2=['Arancia','Pera','Mela','Kiwi','Banana','Arancia','Pera'];SEC=['Mandorle','Noci']*4
PROT=['Yogurt greco 0%:125','Prosciutto cotto:50','Yogurt greco 0%:125','Prosciutto cotto:50','Yogurt greco 0%:125','Yogurt greco 0%:125','Prosciutto cotto:50']
CARB=['Pane integrale:50','Pane integrale:50','Corn flakes:35','Pane integrale:50','Pane integrale:50','Corn flakes:35','Pane integrale:50']
pr=[f"{a},{b},Olio extravergine d’oliva:10,{V[i]}:150!" for i,(a,b) in enumerate(PR)]
ce=[f"{a},{b},Olio extravergine d’oliva:20,{VC[i]}:150!" for i,(a,b) in enumerate(CE)]
sp=[f"{F[i]}:150!,{SEC[i]}:20,Cracker:25,{F2[i]}:150!,{PROT[i]},{CARB[i]}" for i in range(7)]
import json
E=["sce","A scelta, stile nutrizionista","o","equilibrato","A ogni pasto un carboidrato e una proteina presi da un elenco di scelte equivalenti, verdura libera e olio misurato; due spuntini con frutta.",COL,pr,ce,sp]
print(json.dumps(E,ensure_ascii=False))
