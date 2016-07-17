import os
import re
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode

url = "http://menu.ha.ucla.edu/foodpro/cafe1919_summer.asp"

response = urllib.request.urlopen(url)
html = response.read()
soup = bs4.BeautifulSoup(html, 'html.parser')

items = soup.findAll('div', {"class" : lambda x : x and "item" in x })

infos = []

for item in items:
  info = ["", "", "o", ""]

  for child in item.children:

    if child.name == 'span':
      if 'name' in child['class'][0]:
        line = child.text
        line = line.replace(u'\xa0', u'')
        line = line.replace('®', '')
        line = line.replace('™', '')
        line = line.replace('é', 'e')
        info[0] = line

        for cc in child.children:
          # print(cc)
          # get recipe number
          if cc.name == 'a':
            nutritionURL = cc.get('href')
            nutritionURL = re.findall(r'RecipeNumber=\d+', nutritionURL)
            nutritionURL = nutritionURL[0]
            info[3] = nutritionURL[-6:]
          # check if vegetarian or vegan
          for ccc in cc.children:
            if ccc.name == 'img':
              # print(ccc)
              alt = ccc.get('alt')
              # print(alt)
              if "Vegetarian" in alt:
                info[2] = 'v'
              if "Vegan" in alt:
                info[2] = 'g'

      elif 'price' in child['class'][0]:
        price = child.text
        info[1] = price
  
  print(json.dumps(info) + ',')
  infos.append(info)

print(len(infos))

# print(json.dumps(infos))
