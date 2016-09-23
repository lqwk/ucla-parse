# MUST USE FULL PATH FOR CRON JOBS TO WORK
# /home/qingweilan/public_html/cgi-bin

import os
from nutrition import NutritionParser

if __name__ == "__main__":

  path = './nutrition/'
  rs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

  for r in rs:
    parser = NutritionParser(r)
    parser.downloadNutritionData(True)
