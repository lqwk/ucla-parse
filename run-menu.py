import json
import datetime
from parse import Meal
from parse import MenuParser

if __name__ == "__main__":

  dateTime = datetime.datetime.today()
  shouldGetNutrition = True

  for i in range(0, 7):

    currentDate = dateTime + datetime.timedelta(days=i)
    dateString = currentDate.strftime('./menus-nutrition/%Y-%m-%d')
    print(dateString)

    menus = {"b":[],"l":[],"d":[]}

    # breakfast
    meal = Meal.breakfast
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["b"] = menu

    # lunch
    meal = Meal.lunch
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["l"] = menu

    # dinner
    meal = Meal.dinner
    parser = MenuParser(currentDate, meal)
    menu = parser.getMenus(shouldGetNutrition)
    if menu != None:
      menus["d"] = menu

    menuJSON = json.dumps(menus, separators=(',',':'))

    # create file to save to
    file = open(dateString, "w")
    file.write(menuJSON)
    file.close()

    print(menuJSON)
