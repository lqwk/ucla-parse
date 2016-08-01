import json
import datetime
import os

from flask import Flask
from flask import render_template
from flask import request
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
  if 'key' not in request.args or request.args['key'] != APIKey.key:
    return "Wrong API key"

  hoursFile = "./data/hours.json"
  if os.path.exists(hoursFile) and os.path.isfile(hoursFile):
    file = open(hoursFile, "r")
    hoursJSON = file.read()
    file.close()
    return hoursJSON

@app.route('/quick')
def getQuickService():
  if 'key' not in request.args or request.args['key'] != APIKey.key:
    return "Wrong API key"

  quickFile = "./data/quick.json"
  if os.path.exists(quickFile) and os.path.isfile(quickFile):
    file = open(quickFile, "r")
    quickJSON = file.read()
    file.close()
    return quickJSON

@app.route('/menu-nutrition', methods=['GET'])
def getMenuWithNutrition():
  if 'key' not in request.args or request.args['key'] != APIKey.keynu:
    return "Wrong API key"

  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args):
    year = request.args['year']
    month = request.args['month']
    day = request.args['day']

    currentPath = "./menus-nutrition/"
    dateNamePath = currentPath + year + "-" + month + "-" + day

    # check if file exists yet
    if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
      file = open(dateNamePath, "r")
      menuJSON = file.read()
      file.close()
      return menuJSON
    else:
      empty = {"b":[],"l":[],"d":[]}
      return json.dumps(empty, separators=(',',':'))
  # bad parameters
  else:
    empty = {"b":[],"l":[],"d":[]}
    return json.dumps(empty, separators=(',',':'))

@app.route('/menu', methods=['GET'])
def getMenus():
  if 'key' not in request.args or request.args['key'] != APIKey.key:
    return "Wrong API key"

  if ('year' in request.args) and ('month' in request.args) and ('day' in request.args):
    year = request.args['year']
    month = request.args['month']
    day = request.args['day']

    currentPath = "./menus/"
    dateNamePath = currentPath + year + "-" + month + "-" + day

    # check if file exists yet
    if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
      file = open(dateNamePath, "r")
      menuJSON = file.read()
      file.close()
      return menuJSON
    else:
      empty = {"b":[],"l":[],"d":[]}
      return json.dumps(empty, separators=(',',':'))
  # bad parameters
  else:
    empty = {"b":[],"l":[],"d":[]}
    return json.dumps(empty, separators=(',',':'))
