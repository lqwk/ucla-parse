import re
import os
import sys
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode
from enum import Enum
from 'nutrition-parse' import NutritionParser


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
      if tclass != None and len(tclass) != 0 and tclass[0] == 'menulocheader':
        count = count + 1
      else:
        break

    return count


  def separateRestaurants(self, tds):
    """
    Build N containers from 'tds'.

    Depending on the count of valid restaurants, we copy the entries from 'tds'
    into the 'data' array, which will be used later for processing.
    """

    containerCount = self.getRestaurantCount(tds)

    data = []

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
      count = 0
      for td in tds:
        if count == 0:
          data[0].append(td)
        elif count == 1:
          data[1].append(td)
        elif count == 2:
          data[2].append(td)
        elif count == 3:
          data[3].append(td)
        count = count + 1
        if count > 3:
          count = 0

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

    data = self.separateRestaurants(tds)
    if data == None:
      return None

    restaurants = []
    for index, values in enumerate(data):
      restaurant = { kRestaurantName: "", kRestaurantKitchens: [] }
      for d in values:
        # separate the "restaurant name" from the "kitchens"
        for child in d.children:
          if type(child) is bs4.element.Tag:
            childclass = child.get('class')
            if (childclass != None and len(childclass) != 0 and childclass[0] == 'menuloclink'):
              line = child.text.replace(u'\xa0', u'')
              line = line.replace('*', '')
              # print()
              # print('RESTAURANT: ' + line)
              restaurant[kRestaurantName] = line
            else:
              # separate the kitchen name from the entrees
              kitchen = { kKitchenName: "", kKitchenItems: [] }
              for item in child:
                # print(item)
                # print()
                if type(item) is bs4.element.Tag:
                  itemclass = item.get('class')
                  if itemclass != None and len(itemclass) != 0 and ('category' in itemclass[0]):
                    line = item.text.replace(u'\xa0', u'')
                    line = line.replace('*', '')
                    # print()
                    # print('Kitchen: ' + line)
                    kitchen[kKitchenName] = line
                  elif itemclass != None and len(itemclass) != 0 and ('level' in itemclass[0]):
                    # determine whether is 'vegetarian' or 'vegan'
                    itemType = "o"
                    img = item.find('img')
                    if img != None:
                      line = img.get('alt')
                      if "Vegetarian" in line:
                        itemType = 'v'
                      elif "Vegan" in line:
                        itemType = 'g'
                    # get the entree name
                    line = item.text.replace(u'\xa0', u'')
                    line = line.replace('*', '')
                    if line.startswith(("w/", "&")):
                      continue
                    entree = None
                    # determine if we should fetch nutrition data
                    if shouldGetNutrition:
                      # get the link to nutrition data & the nutrition data
                      nutrition = {}
                      nutritionURL = item.find('a').get('href')
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
                          nutritionJSON = parser.downloadNutritionData()
                          nutrition = json.loads(nutritionJSON)
                      entree = { kEntreeName: line, kNutritionData: nutrition, kType: itemType}
                    else:
                      entree = line
                    # print(entree)
                    kitchen[kKitchenItems].append(entree)
              # print(kitchen)
              if kitchen[kKitchenName] != "" and len(kitchen[kKitchenItems]) != 0:
                restaurant[kRestaurantKitchens].append(kitchen)
      if restaurant[kRestaurantName] != "" and len(restaurant[kRestaurantKitchens]) != 0:
        restaurants.append(restaurant)
    # print(restaurants)

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

if __name__ == "__main__":

  dateTime = datetime.datetime.today()
  shouldGetNutrition = True

  for i in range(0, 7):

    currentDate = dateTime + datetime.timedelta(days=i)
    dateString = currentDate.strftime('./menus-nutrition/%Y-%m-%d')
    print(dateString)

    menus = {"b":[],"l":[],"d":[]}

    # breakfast
    meal = NutritionMeal.breakfast
    parser = NutritionMenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["b"] = menu

    # lunch
    meal = NutritionMeal.lunch
    parser = NutritionMenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["l"] = menu

    # dinner
    meal = NutritionMeal.dinner
    parser = NutritionMenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["d"] = menu

    menuJSON = json.dumps(menus, separators=(',',':'))

    # create file to save to
    file = open(dateString, "w")
    file.write(menuJSON)
    file.close()

    print(menuJSON)
