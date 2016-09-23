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

  breakfast = 1
  lunch = 2
  dinner = 3


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

    response = urllib.request.urlopen(self.url)
    html = response.read()
    restaurants = self.parseRestaurantHTML(html, shouldGetNutrition)
    return restaurants


  def getRestaurantCount(self, tds):
    """
    Counts the number of valid restaurants.

    This is achieved by counting the number of entries with the valid
    class called 'menulocheader'.
    """

    count = 0
    for td in tds:
      tclass = td.get('class')
      if tclass and tclass[0] == 'menulocheader':
        count += 1

    return count


  def separateRestaurants(self, tds):
    """
    Build N containers from 'tds'.

    Depending on the count of valid restaurants, we copy the entries from 'tds'
    into the 'data' array, which will be used later for processing.
    """

    containerCount = self.getRestaurantCount(tds)

    data = []

    # TODO: FIX
    if containerCount == 3:
      for i in range(0, 3):
        data.append([])
      count = 0
      for td in tds:
        if count == 0:
          data[0].append(td)
        elif count == 1:
          data[1].append(td)
        elif count == 2:
          data[2].append(td)
        count = count + 1
        if count > 2:
          count = 0


    elif containerCount == 4:
      for i in range(0, 4):
        data.append([])
      cnt, flag = 0, True
      for td in tds:
        # print(td)
        tdclass = td.get('class')
        if tdclass and tdclass[0] == 'menulocheader':
          data[cnt].append(td)
          cnt += 1
          flag = True
          continue
        if cnt <= 2:
          if flag:
            data[0].append(td)
          else:
            data[1].append(td)
          flag = not flag
        elif cnt <= 4:
          if flag:
            data[2].append(td)
          else:
            data[3].append(td)
          flag = not flag

    # TODO: FIX
    elif containerCount == 2:
      for i in range(0, 2):
        data.append([])
      count = 0
      for td in tds:
        if count == 0:
          data[0].append(td)
        elif count == 1:
          data[1].append(td)
        count = count + 1
        if count > 1:
          count = 0

    # TODO: FIX
    elif containerCount == 1:
      data.append([])
      for td in tds:
        data[0].append(td)

    elif containerCount == 0:
      data = None

    return data


  def parseRestaurantHTML(self, html, shouldGetNutrition):
    """
    Parse the 'html' passed in.

    This subroutine uses the open source module 'BeautifulSoup' to parse the
    HTML data.
    The algorithm involved is specific to a certain time period and is not
    applicable to other time periods. If the HTML changes, this will break.
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')

    tds = soup.findAll('td', { "class": lambda x:
      x and (x == "menugridcell" or x == "menugridcell_last" or x == "menulocheader") })

    # print(tds)
    # print(len(tds))
    # for td in tds:
    #   print(td)
    #   print()

    data = self.separateRestaurants(tds)
    if data == None:
      return None

    # for d in data:
    #   print(d)
    #   print()
    #   print()

    restaurants = []
    for index, values in enumerate(data):
      restaurant = { kRestaurantName: "", kRestaurantKitchens: [] }
      for d in values:
        # print(d)
        # print()

        # separate the "restaurant name" from the "kitchens"
        if d.name == 'td':
          dclass = d.get('class')
          if (dclass and dclass[0] == 'menulocheader'):
            for child in d.children:
              if child.name == 'a':
                childclass = child.get('class')
                if (childclass and childclass[0] == 'menuloclink'):
                  line = child.text.replace(u'\xa0', u'')
                  line = line.replace('*', '')
                  # print()
                  # print('RESTAURANT: ' + line)
                  restaurant[kRestaurantName] = line
          elif (dclass and (dclass[0] == 'menugridcell' or dclass[0] == 'menugridcell_last')):
            # print(d)
            # print()

            # separate the kitchen name from the entrees
            kitchen = { kKitchenName: "", kKitchenItems: [] }
            for ul in d:
              if ul.name == 'ul':
                for li in ul:
                  if li.name == 'li':
                    # print(li)
                    # print()
                    liclass = li.get('class')
                    if liclass and 'category' in liclass[0]:
                      line = li.text.replace(u'\xa0', u'')
                      line = line.replace('*', '')
                      # print()
                      # print('KITCHEN: ' + line)
                      kitchen[kKitchenName] = line
                    elif liclass and 'level' in liclass[0]:
                      # determine whether is 'vegetarian' or 'vegan'
                      itemType = "o"
                      img = li.find('img')
                      if img:
                        tp = img.get('alt')
                        if "Vegetarian" in tp:
                          itemType = "v"
                        elif "Vegan" in tp:
                          itemType = "g"
                      # get the entree name
                      line = li.text.replace(u'\xa0', u'')
                      line = line.replace('*', '')
                      if line.startswith(("w/", "&")):
                        continue
                      entree = None
                      # determine if we should fetch nutrition data
                      if shouldGetNutrition:
                        # get the link to nutrition data & the nutrition data
                        nutrition = {}
                        nutritionURL = li.find('a').get('href')
                        nutritionURL = re.findall(r'RecipeNumber=\d+', nutritionURL)
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
                          else:
                            parser = NutritionParser(nutritionURL)
                            nutritionJSON = parser.downloadNutritionData(True)
                            nutrition = json.loads(nutritionJSON)
                        entree = { kEntreeName: line, kNutritionData: nutrition, kType: itemType}
                      else:
                        entree = line
                      # print(entree)
                      kitchen[kKitchenItems].append(entree)
            print(kitchen)
            if kitchen[kKitchenName] != "" and len(kitchen[kKitchenItems]) != 0:
              restaurant[kRestaurantKitchens].append(kitchen)
      print(restaurant)
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

    base = "http://menu.ha.ucla.edu/foodpro/default.asp?"
    meal = meal
    dateString = date.strftime('%m/%d/%Y')
    params = {'date': dateString, 'meal': meal.value, 'threshold': "2"}
    url = base + urlencode(params)
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
