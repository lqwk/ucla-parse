import os
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode
from recipes import Recipes

kCalories = "c"
kFatCalories = "fc"
kVitaminA = "va"
kVitaminC = "vc"
kCalcium = "ca"
kIron = "fe"
kTotalFat = "f"
kSaturatedFat = "sf"
kTransFat = "tf"
kCholesterol = "ch"
kSodium = "s"
kTotalCarbohydrate = "tc"
kDietaryFiber = "df"
kSugars = "ss"
kProtein = "p"


def downloadNutritionData(url):
  """
  Downloads the nutrition data for 'url'
  """

  print(url)

  nutrition = {
    # calories
    kCalories:"0",     # calories
    kFatCalories:"0",  # fat calories
    # vitamins
    kVitaminA:"0%",    # vitamin A
    kVitaminC:"0%",    # vitamin C
    kCalcium:"0%",     # calcium
    kIron:"0%",        # iron
    # other nutrients
    kTotalFat:["0g","0%"],           # total fat
    kSaturatedFat:["0g","0%"],       # saturated fat
    kTransFat:"0g",                  # trans fat
    kCholesterol:["0mg","0%"],       # cholesterol
    kSodium:["0mg","0%"],            # sodium
    kTotalCarbohydrate:["0g","0%"],  # total carbohydrate
    kDietaryFiber:["0g","0%"],       # dietary fiber
    kSugars:"0g",                    # sugars
    kProtein:"0g"                    # protein
  }

  response = urllib.request.urlopen(url)
  html = response.read()
  soup = bs4.BeautifulSoup(html, 'html.parser')


  # find calories
  cals = soup.findAll('p', {"class" : "nfcal"})
  for cal in cals:
    for child in cal.children:
      # print(child)
      if type(child) is bs4.element.NavigableString:
        calories = str(child).strip()
        nutrition[kCalories] = calories
      else:
        childclass = child.get('class')
        if childclass != None and len(childclass) != 0 and childclass[0] == "nffatcal":
          line = child.text
          if "Fat Cal. " in line:
            line = line.replace("Fat Cal. ", "")
            nutrition[kFatCalories] = line

  # find all vitamins
  vits = soup.findAll( "span", { "class" : lambda x:
    x == "nfvitleft" or x == "nfvitright" } )

  for vit in vits:
    vitname = ""
    vitpct = ""
    
    for child in vit:
      if type(child) == bs4.element.Tag:
        childclass = child.get('class')
        if childclass != None and len(childclass) != 0 and childclass[0] == "nfvitname":
          vitname = child.text.strip()
        elif childclass != None and len(childclass) != 0 and childclass[0] == "nfvitpct":
          vitpct = child.text.strip()

    if vitname == "Vitamin A":
      nutrition[kVitaminA] = vitpct
    elif vitname == "Vitamin C":
      nutrition[kVitaminC] = vitpct
    elif vitname == "Calcium":
      nutrition[kCalcium] = vitpct
    elif vitname == "Iron":
      nutrition[kIron] = vitpct

  # find all other nutrient fields
  ps = soup.findAll("p", { "class" : "nfnutrient" })
  if len(ps) != 0:
    for p in ps:
      pct = ""
      line = p.text.strip()

      for child in p:
        if type(child) is bs4.element.Tag:
          childclass = child.get('class')
          if childclass != None and len(childclass) != 0 and childclass[0] == "nfdvval":
            # print("nfdvval", child.text)
            pct = child.text

      if pct != "":
        rp = " " + pct
        line = line.replace(rp, "")

      if "Total Fat " in line:
        line = line.replace("Total Fat ", "")
        nutrition[kTotalFat][0] = line
        nutrition[kTotalFat][1] = pct
      elif "Saturated Fat " in line:
        line = line.replace("Saturated Fat ", "")
        nutrition[kSaturatedFat][0] = line
        nutrition[kSaturatedFat][1] = pct
      elif "Trans Fat " in line:
        line = line.replace("Trans Fat ", "")
        nutrition[kTransFat] = line
      elif "Cholesterol " in line:
        line = line.replace("Cholesterol ", "")
        nutrition[kCholesterol][0] = line
        nutrition[kCholesterol][1] = pct
      elif "Sodium " in line:
        line = line.replace("Sodium ", "")
        nutrition[kSodium][0] = line
        nutrition[kSodium][1] = pct
      elif "Total Carbohydrate " in line:
        line = line.replace("Total Carbohydrate ", "")
        nutrition[kTotalCarbohydrate][0] = line
        nutrition[kTotalCarbohydrate][1] = pct
      elif "Dietary Fiber " in line:
        line = line.replace("Dietary Fiber ", "")
        nutrition[kDietaryFiber][0] = line
        nutrition[kDietaryFiber][1] = pct
      elif "Sugars " in line:
        line = line.replace("Sugars ", "")
        nutrition[kSugars] = line
      elif "Protein " in line:
        line = line.replace("Protein ", "")
        nutrition[kProtein] = line


  nutritionJSON = json.dumps(nutrition, separators=(',',':'))
  # print(json.dumps(nutrition, indent=2))

  # create file to save to
  file = open(filename, "w")
  file.write(nutritionJSON)
  file.close()


if __name__ == "__main__":

  base = "http://menu.ha.ucla.edu/foodpro/recipedetail.asp?RecipeNumber="
  filebase = "./nutrition/"

  for r in Recipes.recipes:

    url = base + r
    filename = filebase + r

    # check if file exists yet
    if os.path.exists(filename) and os.path.isfile(filename):
      # if exists, check the time stamp
      statinfo = os.stat(filename)
      filetime = datetime.datetime.fromtimestamp(statinfo.st_mtime)
      servertime = datetime.datetime.now()
      td = servertime - filetime
      diffdays = td.days
      # if the time difference is greater than 4 days, re-download
      if diffdays >= 4:
        downloadNutritionData(url)
    else:
      downloadNutritionData(url)
