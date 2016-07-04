#!/home/qingweilan/.local/bin/python3
from wsgiref.handlers import CGIHandler
from menuapp import app

CGIHandler().run(app)
