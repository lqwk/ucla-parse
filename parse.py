import sys
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode
from enum import Enum


# constants
kRestaurantName = "r"
kRestaurantKitchens = "rk"
kKitchenName = "k"
kKitchenItems = "i"
kEntreeName = "e"
kNutritionData = "n"

class Meal(Enum):
  """
  Meal enumeration class used for passing in data to 'MenuParser'
  """

  breakfast = 1
  lunch = 2
  dinner = 3

  @classmethod
  def getMeal(meal, m):
    """
    Class method for parsing strings and returning corresponding Meal class
    """

    if m == 'b':
      return meal.breakfast
    elif m == 'l':
      return meal.lunch
    elif m == 'd':
      return meal.dinner


class MenuParser:
  """
  Menu parser class which holds 'date', 'meal', and 'url'

  Used to fetch html data from the web and parse it to build JSON data
  """

  def __init__(self, date, meal):
    self.date = date
    self.meal = meal
    self.url = self.buildURL(date, meal)


  def getMenus(self):
    """
    Executes the menu fetch.

    Reads the html data fetched from 'self.url'.
    Then parses the html data.
    """

    response = urllib.request.urlopen(self.url)
    html = response.read()
    restaurants = self.parseRestaurantHTML(html)
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


  def parseRestaurantHTML(self, html):
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
                    # get the entree name
                    line = item.text.replace(u'\xa0', u'')
                    line = line.replace('*', '')
                    if line.startswith(("w/", "&")):
                      continue
                    # print('e: ' + line)
                    kitchen[kKitchenItems].append(line)
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

  for i in range(0, 7):

    currentDate = dateTime + datetime.timedelta(days=i)
    dateString = currentDate.strftime('./menus/%Y-%m-%d')
    print(dateString)

    menus = {"b":[],"l":[],"d":[]}

    # breakfast
    meal = Meal.breakfast
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus()
    if menu != None:
      menus["b"] = menu

    # lunch
    meal = Meal.lunch
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus()
    if menu != None:
      menus["l"] = menu

    # dinner
    meal = Meal.dinner
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus()
    if menu != None:
      menus["d"] = menu

    menuJSON = json.dumps(menus, separators=(',',':'))

    # create file to save to
    file = open(dateString, "w")
    file.write(menuJSON)
    file.close()

    print(menuJSON)
