import os
import json

from nutrition import NutritionParser

file = open('./data/quick.json', 'r')
quickJSON = file.read()
file.close()
quick = json.loads(quickJSON)

for key, menu in quick.items():
  for k in range(0, len(menu)):
    kitchen = menu[k]
    for i in range(1, len(kitchen)):
      section = kitchen[i]
      for j in range(2, len(section)):
        entree = section[j]
        recipe = entree[3]
        
        nutritionPath = './nutrition/' + recipe
        nutrition = []
        if os.path.exists(nutritionPath) and os.path.isfile(nutritionPath):
          file = open(nutritionPath, 'r')
          nutritionJSON = file.read()
          file.close()
          nutrition = json.loads(nutritionJSON)
        else:
          parser = NutritionParser(recipe)
          nutritionJSON = parser.downloadNutritionData()
          nutrition = json.loads(nutritionJSON)
        quick[key][k][i][j][3] = nutrition
        # print(entree)

print(quick)
quickJSON = json.dumps(quick, separators=(',',':'))
file = open('./data/quick.min.json', 'w')
file.write(quickJSON)
file.close()
