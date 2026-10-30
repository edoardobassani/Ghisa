import csv,json
B='/home/claude/dl/src/sr/FoodData_Central_sr_legacy_food_csv_2018-04/'
food={r['fdc_id']:r['description'] for r in csv.DictReader(open(B+'food.csv'))}
M={'1008':'kcal','1003':'p','1005':'c','1004':'f','1079':'fib','2000':'sug','1093':'na','1092':'k','1087':'ca','1090':'mg','1089':'fe','1162':'vc','1095':'zn','1178':'b12','1114':'d'}
D={i:{'code':i,'name':n} for i,n in food.items()}
for r in csv.DictReader(open(B+'food_nutrient.csv')):
  k=M.get(r['nutrient_id'])
  if k and r['fdc_id'] in D:D[r['fdc_id']][k]=float(r['amount'])
json.dump(list(D.values()),open('/home/claude/dl/usda.json','w'));print(len(D))
