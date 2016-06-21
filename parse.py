import bs4

from enum import Enum
class Meal(Enum):
	breakfast = 1
	lunch = 2
	dinner = 3

from urllib.parse import urlparse
from urllib.parse import urlencode
import re


def parseHTML(html):
	"""Parse the 'html' passed in."""

	soup = bs4.BeautifulSoup(html, 'html.parser')

	tds = soup.findAll('td', { "class": lambda x: 
		x and (x == "menugridcell" or x == "menugridcell_last" or x == "menulocheader") })

	if len(tds) % 3 == 0:
		count = 0
		data = [[], [], []]
		menu = [[], [], []]

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


		for index, values in enumerate(data):
			for d in values:
				# separate the "restaurant name" from the "kitchens"
				for child in d.children:
					if type(child) is bs4.element.Tag:
						childclass = child.get('class')
						if (childclass != None and len(childclass) != 0 and childclass[0] == 'menuloclink'):
							line = child.text.replace(u'\xa0', u'')
							line = line.replace('*', '')
							print()
							print('RESTAURANT: ' + line)
						else:
							# separate the kitchen name from the entrees
							for item in child:
								if type(item) is bs4.element.Tag:
									itemclass = item.get('class')
									if itemclass != None and len(itemclass) != 0 and ('category' in itemclass[0]):
										line = item.text.replace(u'\xa0', u'')
										line = line.replace('*', '')
										print()
										print('Kitchen: ' + line)
									elif itemclass != None and len(itemclass) != 0 and ('level' in itemclass[0]):
										line = item.text.replace(u'\xa0', u'')
										line = line.replace('*', '')
										print('e: ' + line)


					# print(type(child))
					# print(child)
				# for itemList in d:
				# 	for item in itemList:

				# 		print(item)
				# 		print(type(item))
				# 		# print(item.attrs)
				# 		print()



				# text = d.text
				# print(text)
				# print()
				# if text.strip() != "":
				# 	# print(text)
				# 	# print()
				# 	lines = []
				# 	for line in text.split('\n'):
				# 		if line.strip() != "":
				# 			line = line.replace(u'\xa0', u'')
				# 			line = line.replace('*', '')
				# 			if not re.match('^w/', line):
				# 				# print(line)
				# 				lines.append(line)
				# 	# print()
				# 	menu[index].append(lines)

	elif len(tds) % 2 == 0:
		print("not handled")

	return menu

from datetime import date

def buildURL(date, meal):
	"""Build URL from 'date' and 'meal'."""

	base = "http://menu.ha.ucla.edu/foodpro/default.asp?"
	meal = meal
	dateString = date.strftime('%m/%d/%Y')
	print(dateString)
	params = {'date': dateString, 'meal': meal.value, 'threshold': "2"}
	url = base + urlencode(params)
	return url


url = buildURL(date.today(), Meal.dinner)
print(url)

import json

import urllib.request
with urllib.request.urlopen(url) as response:
	html = response.read()
	# parseHTML(html)
	menu = parseHTML(html)
	# print(json.dumps(menu, indent=4))

