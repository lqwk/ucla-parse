import json
import datetime
import os

from flask import Flask
from flask import render_template
from flask import request
from parse import Meal
from parse import MenuParser

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
@app.route('/home')
@app.route('/index')
def showIndexPage():
  return render_template('index.html')

@app.route('/menu', methods=['GET'])
def getMenus():
  error = None
  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args):
    year = request.args['year']
    month = request.args['month']
    day = request.args['day']

    currentPath = "./menus/"
    dateNamePath = currentPath + year + "-" + month + "-" + day

    # create directory to hold menus
    os.makedirs(currentPath,exist_ok=True)

    # check if file exists yet
    if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
      # if exists, just read the file and return
      file = open(dateNamePath, "r")
      menuJSON = file.read()
      file.close()
      return menuJSON

    else:
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

      menuJSON = json.dumps(menus)

      # create file to save to
      file = open(dateNamePath, "w")
      file.write(menuJSON)
      file.close()

      return menuJSON

  else:
    return "Bad parameters"
