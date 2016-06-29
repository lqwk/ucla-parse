from flask import Flask
from flask import render_template
from flask import request

import json
import datetime
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
  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args) and ('meal' in request.args):
    year = int(float(request.args['year']))
    month = int(float(request.args['month']))
    day = int(float(request.args['day']))
    m = request.args['meal']

    dateTime = datetime.date(year, month, day)
    meal = Meal.getMeal(m)
    parser = MenuParser(dateTime, meal)
    menus = parser.getMenus()

    return json.dumps(menus)
  else:
    return "Bad parameters"
