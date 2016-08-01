import os
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode
from recipes import Recipes

kCalories = 0
kFatCalories = 1

kVitaminA = 2
kVitaminC = 3
kCalcium = 4
kIron = 5

kTotalFat = 6
kTotalFatPCT = 7
kSaturatedFat = 8
kSaturatedFatPCT = 9
kTransFat = 10

kCholesterol = 11
kCholesterolPCT = 12
kSodium = 13
kSodiumPCT = 14

kTotalCarbohydrate = 15
kTotalCarbohydratePCT = 16
kDietaryFiber = 17
kDietaryFiberPCT = 18

kSugars = 19
kProtein = 20

class NutritionParser:

  def __init__(self, recipe):
    self.recipe = recipe

  def downloadNutritionDataForURL(self, url, shouldSave, filename):
    """
    Downloads the nutrition data for 'url' and saves to 'filename'
    """

    print(url)

    nutrition = ["0"] * (kProtein+1)

    nutrition[kVitaminA] = "0%"
    nutrition[kVitaminC] = "0%"
    nutrition[kCalcium] = "0%"
    nutrition[kIron] = "0%"
    nutrition[kTotalFat] = "0g"
    nutrition[kTotalFatPCT] = "0%"
    nutrition[kSaturatedFat] = "0g"
    nutrition[kSaturatedFatPCT] = "0%"
    nutrition[kTransFat] = "0g"
    nutrition[kCholesterol] = "0mg"
    nutrition[kCholesterolPCT] = "0%"
    nutrition[kSodium] = "0mg"
    nutrition[kSodiumPCT] = "0%"
    nutrition[kTotalCarbohydrate] = "0g"
    nutrition[kTotalCarbohydratePCT] = "0%"
    nutrition[kDietaryFiber] = "0g"
    nutrition[kDietaryFiberPCT] = "0%"
    nutrition[kSugars] = "0g"
    nutrition[kProtein] = "0g"

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
          nutrition[kTotalFat] = line
          nutrition[kTotalFatPCT] = pct
        elif "Saturated Fat " in line:
          line = line.replace("Saturated Fat ", "")
          nutrition[kSaturatedFat] = line
          nutrition[kSaturatedFatPCT] = pct
        elif "Trans Fat " in line:
          line = line.replace("Trans Fat ", "")
          nutrition[kTransFat] = line
        elif "Cholesterol " in line:
          line = line.replace("Cholesterol ", "")
          nutrition[kCholesterol] = line
          nutrition[kCholesterolPCT] = pct
        elif "Sodium " in line:
          line = line.replace("Sodium ", "")
          nutrition[kSodium] = line
          nutrition[kSodiumPCT] = pct
        elif "Total Carbohydrate " in line:
          line = line.replace("Total Carbohydrate ", "")
          nutrition[kTotalCarbohydrate] = line
          nutrition[kTotalCarbohydratePCT] = pct
        elif "Dietary Fiber " in line:
          line = line.replace("Dietary Fiber ", "")
          nutrition[kDietaryFiber] = line
          nutrition[kDietaryFiberPCT] = pct
        elif "Sugars " in line:
          line = line.replace("Sugars ", "")
          nutrition[kSugars] = line
        elif "Protein " in line:
          line = line.replace("Protein ", "")
          nutrition[kProtein] = line

    for i in range(0, len(nutrition)):
      nutrition[i] = nutrition[i].replace('--', '0')

    nutritionJSON = json.dumps(nutrition, separators=(',',':'))

    # print(nutritionJSON)

    # create file to save to
    if shouldSave and filename != None:
      file = open(filename, "w")
      file.write(nutritionJSON)
      file.close()

    return nutritionJSON

  def downloadNutritionData(self, shouldSave=False, filebase='./nutrition/'):
    """
    Downloads the nutrition data for recipe number 'recipe'.

    First it checks if the nutrition data exists and is up to date.
    If not, then it downloads the nutrition data from the UCLA site.
    """

    base = "http://menu.ha.ucla.edu/foodpro/recipedetail.asp?RecipeNumber="

    url = base + self.recipe
    filename = None

    if shouldSave:
      filename = filebase + self.recipe
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
          return self.downloadNutritionDataForURL(url, shouldSave, filename)
      else:
        return self.downloadNutritionDataForURL(url, shouldSave, filename)

    else:
      return self.downloadNutritionDataForURL(url, shouldSave, filename)


if __name__ == "__main__":

  path = './nutrition/'
  rs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

  for r in rs:
    parser = NutritionParser(r)
    parser.downloadNutritionData(True)
