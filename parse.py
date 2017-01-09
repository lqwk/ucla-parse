# MUST USE FULL PATH FOR CRON JOBS TO WORK
# /home/qingweilan/public_html/cgi-bin

import re
import os
import sys
import bs4
import json
import datetime
import argparse
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode
from enum import Enum
from nutrition import NutritionParser


# constants
kRestaurantName = "r"
kRestaurantKitchens = "rk"
kKitchenName = "k"
kKitchenItems = "i"
kEntreeName = "e"
kNutritionData = "n"
kType = "t"

class Meal(Enum):
  """
  Meal enumeration class used for passing in data to 'MenuParser'
  """

  breakfast = "Breakfast"
  lunch = "Lunch"
  dinner = "Dinner"


class MenuParser:
  """
  Menu parser class which holds 'date', 'meal', and 'url'

  Used to fetch html data from the web and parse it to build JSON data
  """

  def __init__(self, date, meal):
    self.date = date
    self.meal = meal
    self.url = self.buildURL(date, meal)


  def getMenus(self, shouldGetNutrition):
    """
    Executes the menu fetch.

    Reads the html data fetched from 'self.url'.
    Then parses the html data.
    """

    print(self.url)
    response = urllib.request.urlopen(self.url)
    html = response.read()
    restaurants = self.parseRestaurantHTML(html, shouldGetNutrition)
    return restaurants


  def parseRestaurantHTML(self, html, shouldGetNutrition):
    """
    Parse the 'html' passed in.

    This subroutine uses the open source module 'BeautifulSoup' to parse the
    HTML data.
    The algorithm involved is specific to a certain time period and is not
    applicable to other time periods. If the HTML changes, this will break.
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')

    divs = soup.findAll('div', { "class": "menu-block" })

    # print(divs)
    print(len(divs))

    restaurants = []
    for div in divs:
      restaurant = { kRestaurantName: "", kRestaurantKitchens: [] }

      for child in div.children:

        # get the restaurant name
        if child.name == 'h3':
          cc = child.get('class')
          if cc and cc[0] == 'col-header':
            restaurantName = child.text
            restaurant[kRestaurantName] = restaurantName
            # print('RESTAURANT: ' + restaurantName)
        
        # get the list of kitchens
        if child.name == 'ul':
          cc = child.get('class')
          if cc and cc[0] == 'sect-list':
            for item in child:
              if item.name == 'li':
                ic = item.get('class')
                if ic and ic[0] == 'sect-item':
                  kitchen = { kKitchenName: "", kKitchenItems: [] }
                  for ii in item:
                    
                    # name of kitchen
                    if isinstance(ii, bs4.element.NavigableString):
                      kitchenName = str(ii)
                      kitchenName = kitchenName.strip()
                      if kitchenName == "":
                        continue
                      kitchen[kKitchenName] = kitchenName
                      # print('KITCHEN: ' + kitchenName)
                    
                    # items in the kitchen
                    elif ii.name == 'ul':
                      iic = ii.get('class')
                      if iic and iic[0] == 'item-list':
                        for menuitem in ii:
                          if menuitem.name == 'li':
                            menuitemc = menuitem.get('class')
                            if menuitemc and menuitemc[0] == 'menu-item':
                              entree = None

                              # find the item name & recipe
                              iteminfo = menuitem.find('span')
                              if iteminfo:
                                entreeName = iteminfo.text.strip()
                                entreeName = entreeName.replace(u'\xa0', u'')
                                entreeName = entreeName.replace('*', '')
                                if entreeName.startswith(("w/", "&")):
                                  continue
                                # print('ENTREE NAME: ' + entreeName)

                                # don't need nutrition information
                                if not shouldGetNutrition:
                                  entree = entreeName

                                # need to find nutrition information
                                else:
                                  # allergy information
                                  # ALLERGY INFO ENCODING SCHEMA
                                  #
                                  # v, g: (V) vegetarian, (VG) vegan
                                  #
                                  # p : (APNT) peanuts
                                  # t : (ATNT) tree nuts
                                  # w : (AWHT) wheat
                                  # s : (ASOY) soy
                                  # d : (AMLK) dairy
                                  # e : (AEGG) eggs
                                  # l : (ACSF) shellfish
                                  # f : (AFSH) fish
                                  # c : (LC) low-carbon footprint 

                                  itemType = ""
                                  imgs = iteminfo.findAll('img')
                                  if imgs:
                                    for img in imgs:
                                      alt = img.get('alt')
                                      if alt == "V":
                                        itemType = itemType + "v"
                                      elif alt == "VG":
                                        itemType = itemType + "g"
                                      elif alt == "APNT":
                                        itemType = itemType + "p"
                                      elif alt == "ATNT":
                                        itemType = itemType + "t"
                                      elif alt == "AWHT":
                                        itemType = itemType + "w"
                                      elif alt == "ASOY":
                                        itemType = itemType + "s"
                                      elif alt == "AMLK":
                                        itemType = itemType + "d"
                                      elif alt == "AEGG":
                                        itemType = itemType + "e"
                                      elif alt == "ACSF":
                                        itemType = itemType + "l"
                                      elif alt == "AFSH":
                                        itemType = itemType + "f"
                                      elif alt == "LC":
                                        itemType = itemType + "c"

                                  # get the link to nutrition data & the nutrition data
                                  nutrition = {}
                                  nutritionURL = iteminfo.find('a').get('href')
                                  nutritionURL = re.findall(r'Recipes/\d+', nutritionURL)
                                  if nutritionURL != None and len(nutritionURL) != 0:
                                    nutritionURL = nutritionURL[0]
                                    nutritionURL = nutritionURL[-6:]
                                  if nutritionURL != None and len(nutritionURL) == 6:
                                    # print(nutritionURL)
                                    nutritionPath = './nutrition/' + nutritionURL
                                    if os.path.exists(nutritionPath) and os.path.isfile(nutritionPath):
                                      file = open(nutritionPath, 'r')
                                      nutritionJSON = file.read()
                                      file.close()
                                      nutrition = json.loads(nutritionJSON)
                                      # print(nutrition)
                                    else:
                                      parser = NutritionParser(nutritionURL)
                                      nutritionJSON = parser.downloadNutritionData(True)
                                      nutrition = json.loads(nutritionJSON)
                                      # print(nutrition)

                                  # construct the entree
                                  entree = { kEntreeName: entreeName, kNutritionData: nutrition, kType: itemType}
                            if entree != None and entreeName != "":
                              # print(entree)
                              kitchen[kKitchenItems].append(entree)

                  # print(kitchen)
                  if kitchen[kKitchenName] != "" and len(kitchen[kKitchenItems]) != 0:
                    restaurant[kRestaurantKitchens].append(kitchen)
        
      # print(restaurant)
      if restaurant[kRestaurantName] != "" and len(restaurant[kRestaurantKitchens]) != 0:
        restaurants.append(restaurant)

    # print(json.dumps(restaurants,indent=2))

    return restaurants


  def buildURL(self, date, meal):
    """
    Build URL from 'date' and 'meal'.

    Builds a url for the parser to get the menu data.
    The url depends on the 'Meal' (either breakfast, lunch, or dinner)
    and the data for which the menu is supposed be for.
    """

    base = "http://menu.dining.ucla.edu/Menus/"
    meal = meal
    dateString = date.strftime('%Y-%m-%d')
    url = base + dateString + "/" + meal.value
    return url


def downloadMenu(date, dateString, meal, shouldGetNutrition):
  """
  Downloads menu for 'date' for 'meal'
  """

  if shouldGetNutrition:
    if meal == Meal.breakfast:
      print("Downloading menus with nutrition for: " + dateString + " [BREAKFAST]")
    elif meal == Meal.lunch:
      print("Downloading menus with nutrition for: " + dateString + " [LUNCH]")
    elif meal == Meal.dinner:
      print("Downloading menus with nutrition for: " + dateString + " [DINNER]")
  else:
    if meal == Meal.breakfast:
      print("Downloading menus for: " + dateString + " [BREAKFAST]")
    elif meal == Meal.lunch:
      print("Downloading menus for: " + dateString + " [LUNCH]")
    elif meal == Meal.dinner:
      print("Downloading menus for: " + dateString + " [DINNER]")

  parser = MenuParser(date, meal)
  menu = parser.getMenus(shouldGetNutrition)
  if not menu:
    return []
  return menu


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("year", help="year of the menu data you wish to download", type=int)
  parser.add_argument("month", help="month of the menu data you wish to download", type=int)
  parser.add_argument("day", help="month of the menu data you wish to download", type=int)
  parser.add_argument("-n", "--nutrition", help="determine whether to download nutrition data", action="store_true")
  parser.add_argument("-b", "--breakfast", help="download breakfast menus", action="store_true")
  parser.add_argument("-l", "--lunch", help="download lunch menus", action="store_true")
  parser.add_argument("-d", "--dinner", help="download dinner menus", action="store_true")

  args = parser.parse_args()

  shouldGetNutrition = False
  if args.nutrition:
    shouldGetNutrition = True

  menus = {"b":[],"l":[],"d":[]}

  date = datetime.date(args.year, args.month, args.day)
  dateString = str(args.year)+'-'+str(args.month)+'-'+str(args.day)

  if (not args.breakfast) and (not args.lunch) and (not args.dinner):
    menus["b"] = downloadMenu(date, dateString, Meal.breakfast, shouldGetNutrition)
    menus["l"] = downloadMenu(date, dateString, Meal.lunch, shouldGetNutrition)
    menus["d"] = downloadMenu(date, dateString, Meal.dinner, shouldGetNutrition)
  else:
    if args.breakfast:
      menus["b"] = downloadMenu(date, dateString, Meal.breakfast, shouldGetNutrition)
    if args.lunch:
      menus["l"] = downloadMenu(date, dateString, Meal.lunch, shouldGetNutrition)
    if args.dinner:
      menus["d"] = downloadMenu(date, dateString, Meal.dinner, shouldGetNutrition)

  menuJSON = json.dumps(menus, separators=(',',':'))
  print(menuJSON)
