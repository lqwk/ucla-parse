from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
@app.route('/home')
@app.route('/index')
def showIndexPage():
  return render_template('index.html')
