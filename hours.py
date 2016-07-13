import sys
import bs4
import json
import datetime
import urllib.request

from urllib.parse import urlparse
from urllib.parse import urlencode


def getStoreHours():
  """
  Fetch UCLA store hours.
  """

  hours = []

  url = "http://asucla.ucla.edu/ucla-store-hours/"
  # print(url)

  response = urllib.request.urlopen(url)
  html = response.read()
  soup = bs4.BeautifulSoup(html, 'html.parser')

  trs = soup.findAll('tr', { "class": "atable1" })

  for tr in trs:
    details = []
    phone = ""
    for td in tr.children: # get all tds in the tr
      if type(td) != bs4.element.NavigableString:
        for child in td.children:
          if child.name == "a":
            phone = child.text
          elif type(child) == bs4.element.NavigableString:
            line = child.strip()
            if line != "":
              details.append(line)
          else:
            line = child.text.strip()
            if line != "":
              details.append(line)
    details.append(phone)
    
    for i in range(2, 7):
      line = details[i].replace(u'a', u' AM')
      line = line.replace(u'\xa0', u'')
      line = line.replace(u'p', u' PM')
      line = line.replace(u'- ', u' - ')
      line = line.replace(u'M-', u'M - ')
      line = line.replace(u' – ', u' - ')
      details[i] = line

    info = {
      "kName" : details[0],
      "kLocation" : details[1],
      "kPhone": details[7],
      "kHours" : [
        details[2],
        details[2],
        details[3],
        details[3],
        details[4],
        details[5],
        details[6]
      ]
    }

    hours.append(info)

  return hours
          

def getRestaurantHours():
  """
  Fetch UCLA restaurant hours.
  """

  hours = []

  url = "http://asucla.ucla.edu/ucla-restaurant-hours/"
  # print(url)

  response = urllib.request.urlopen(url)
  html = response.read()
  soup = bs4.BeautifulSoup(html, 'html.parser')

  trs = soup.findAll('tr', { "class": "atable1" })

  for tr in trs:
    details = []
    for td in tr.children: # get all tds in the tr
      if type(td) != bs4.element.NavigableString:
        for child in td.children:
          if type(child) == bs4.element.NavigableString:
            line = child.strip()
            if line != "":
              details.append(line)
          else:
            line = child.text.strip()
            if line != "":
              details.append(line)
    
    # fix 'cafe' encoding problem
    details[0] = details[0].replace(u'\u00e9', u'e')
    # fix \' encoding problem
    details[0] = details[0].replace(u'\u2019', u'\'')

    for i in range(3, 7):
      line = details[i].replace(u'a', u' AM')
      line = line.replace(u'p', u' PM')
      line = line.replace(u'-', u' - ')
      line = line.replace(u' – ', u' - ')
      line = line.replace(u'\u2013\u00a0', u'- ')
      details[i] = line

    info = {
      "kName" : details[0],
      "kLocation" : details[1],
      "kPhone": details[2],
      "kHours" : [
        details[3],
        details[3],
        details[3],
        details[3],
        details[4],
        details[5],
        details[6]
      ]
    }

    hours.append(info)

  return hours


if __name__ == "__main__":

  info = {
    "kRestaurantHours" : getRestaurantHours(),
    "kStoreHours" : getStoreHours()
  }

  print(json.dumps(info, indent=2))
