import json
import datetime
import os
import nutrition

from flask import Flask
from flask import render_template
from flask import request
from parse import Meal
from parse import MenuParser
from nuparse import NutritionMeal
from nuparse import NutritionMenuParser
from key import APIKey

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
@app.route('/home')
@app.route('/index')
def showIndexPage():
  return render_template('index.html')

@app.route('/hours')
def getHours():
  logfile = open("./logfile", "a")
  currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  route = 'hours'
  header = '[{0}] [{1}]: '.format(currentTime, route)

  if 'key' not in request.args or request.args['key'] != APIKey.key:
    log = header + "wrong API key, access denied\n"
    logfile.write(log)
    logfile.close()
    return "Wrong API key"

  log = header + "GET hours\n"
  logfile.write(log)
  logfile.close()

  hoursFile = "./data/hours.json"
  if os.path.exists(hoursFile) and os.path.isfile(hoursFile):
    file = open(hoursFile, "r")
    hoursJSON = file.read()
    file.close()
    return hoursJSON

@app.route('/quick')
def getQuickService():
  logfile = open("./logfile", "a")
  currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  route = 'quick'
  header = '[{0}] [{1}]: '.format(currentTime, route)

  if 'key' not in request.args or request.args['key'] != APIKey.key:
    log = header + "wrong API key, access denied\n"
    logfile.write(log)
    logfile.close()
    return "Wrong API key"

  log = header + "GET quick\n"
  logfile.write(log)
  logfile.close()

  quickFile = "./data/quick.json"
  if os.path.exists(quickFile) and os.path.isfile(quickFile):
    file = open(quickFile, "r")
    quickJSON = file.read()
    file.close()
    return quickJSON

@app.route('/menu-nutrition', methods=['GET'])
def getMenuWithNutrition():
  logfile = open("./logfile", "a")
  currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  route = 'menu-nutrition'
  header = '[{0}] [{1}]: '.format(currentTime, route)

  if 'key' not in request.args or request.args['key'] != APIKey.keynu:
    log = header + "wrong API key, access denied\n"
    logfile.write(log)
    logfile.close()
    return "Wrong API key"

  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args):
    year = request.args['year']
    month = request.args['month']
    day = request.args['day']

    param = "{0}-{1}-{2}".format(year, month, day)
    log = header + "GET menu-nutrition: " + param + "\n"
    logfile.write(log)
    logfile.close()

    currentPath = "./menus-nutrition/"
    dateNamePath = currentPath + year + "-" + month + "-" + day

    # create directory to hold menus
    os.makedirs(currentPath,exist_ok=True)

    # check if file exists yet
    if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
      # if exists, check the time stamp
      statinfo = os.stat(dateNamePath)
      filetime = datetime.datetime.fromtimestamp(statinfo.st_mtime)
      servertime = datetime.datetime.now()
      td = servertime - filetime
      diffhours = td.days*24 + td.seconds/3600
      # if the time difference is less than 2 hours, return the stored data
      if diffhours <= 2.0:
        file = open(dateNamePath, "r")
        menuJSON = file.read()
        file.close()
        return menuJSON
      # otherwise, re-download and save the data
      else:
        menuJSON = fetchMenuNutrition(year, month, day, dateNamePath)
        return menuJSON
    # file does not exist
    else:
      menuJSON = fetchMenuNutrition(year, month, day, dateNamePath)
      return menuJSON
  # bad parameters
  else:
    log = header + "GET menu-nutrition: bad parameters\n"
    logfile.write(log)
    logfile.close()
    return "Bad parameters"

@app.route('/menu', methods=['GET'])
def getMenus():
  logfile = open("./logfile", "a")
  currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  route = 'menu'
  header = '[{0}] [{1}]: '.format(currentTime, route)

  if 'key' not in request.args or request.args['key'] != APIKey.key:
    log = header + "wrong API key, access denied\n"
    logfile.write(log)
    logfile.close()
    return "Wrong API key"

  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args):
    year = request.args['year']
    month = request.args['month']
    day = request.args['day']

    param = "{0}-{1}-{2}".format(year, month, day)
    log = header + "GET menu: " + param + "\n"
    logfile.write(log)
    logfile.close()

    currentPath = "./menus/"
    dateNamePath = currentPath + year + "-" + month + "-" + day

    # create directory to hold menus
    os.makedirs(currentPath,exist_ok=True)

    # check if file exists yet
    if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
      # if exists, check the time stamp
      statinfo = os.stat(dateNamePath)
      filetime = datetime.datetime.fromtimestamp(statinfo.st_mtime)
      servertime = datetime.datetime.now()
      td = servertime - filetime
      diffhours = td.days*24 + td.seconds/3600
      # if the time difference is less than 2 hours, return the stored data
      if diffhours <= 2.0:
        file = open(dateNamePath, "r")
        menuJSON = file.read()
        file.close()
        return menuJSON
      # otherwise, re-download and save the data
      else:
        menuJSON = fetchMenu(year, month, day, dateNamePath)
        return menuJSON
    # file does not exist
    else:
      menuJSON = fetchMenu(year, month, day, dateNamePath)
      return menuJSON
  # bad parameters
  else:
    log = header + "GET menu: bad parameters\n"
    logfile.write(log)
    logfile.close()
    return "Bad parameters"

def fetchMenu(year, month, day, dateNamePath):
  """
  Routine used to fetch and save menu data.
  """

  try:
    dateTime = datetime.date(int(float(year)), int(float(month)), int(float(day)))
  except:
    return "Bad date"

  menus = {"b":[],"l":[],"d":[]}

  # breakfast
  meal = Meal.breakfast
  parser = MenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["b"] = menu

  # lunch
  meal = Meal.lunch
  parser = MenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["l"] = menu

  # dinner
  meal = Meal.dinner
  parser = MenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["d"] = menu

  menuJSON = json.dumps(menus, separators=(',',':'))

  # create file to save to
  file = open(dateNamePath, "w")
  file.write(menuJSON)
  file.close()

  return menuJSON

def fetchMenuNutrition(year, month, day, dateNamePath):
  """
  Routine used to fetch and save menu data (with nutrition data).
  """

  try:
    dateTime = datetime.date(int(float(year)), int(float(month)), int(float(day)))
  except:
    return "Bad date"

  menus = {"b":[],"l":[],"d":[]}

  # breakfast
  meal = NutritionMeal.breakfast
  parser = NutritionMenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["b"] = menu

  # lunch
  meal = NutritionMeal.lunch
  parser = NutritionMenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["l"] = menu

  # dinner
  meal = NutritionMeal.dinner
  parser = NutritionMenuParser(dateTime, meal)
  menu = parser.getMenus()
  if menu != None:
    menus["d"] = menu

  menuJSON = json.dumps(menus, separators=(',',':'))

  # create file to save to
  file = open(dateNamePath, "w")
  file.write(menuJSON)
  file.close()

  return menuJSON
