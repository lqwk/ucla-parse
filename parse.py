import bs4

from enum import Enum
class Meal(Enum):
	breakfast = 1
	lunch = 2
	dinner = 3

from urllib.parse import urlparse
from urllib.parse import urlencode
import re


restaurantName = "restaurantName"
restaurantKitchens = "restaurantKitchens"
kitchenName = "kitchenName"
kitchenItems = "kitchenItems"


def getCountOfContainers(tds):
	"""
	Counts the number of valid restaurants.

	This is achieved by counting the number of entries with the valid
	class called 'menulocheader'.
	"""

	count = 0
	for td in tds:
		tclass = td.get('class')
		if tclass != None and len(tclass) != 0 and tclass[0] == 'menulocheader':
			count = count + 1
		else:
			break

	return count

def buildDataContainer(tds):
	"""
	Build N containers from 'tds'.

	Depending on the count of valid restaurants, we copy the entries from 'tds'
	into the 'data' array, which will be used later for processing.
	"""

	containerCount = getCountOfContainers(tds)

	data = []

	if containerCount == 3:
		for i in range(0, 3):
			data.append([])
		count = 0
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

	elif containerCount == 4:
		for i in range(0, 4):
			data.append([])
		count = 0
		for td in tds:
			if count == 0:
				data[0].append(td)
			elif count == 1:
				data[1].append(td)
			elif count == 2:
				data[2].append(td)
			elif count == 3:
				data[3].append(td)
			count = count + 1
			if count > 3:
				count = 0

	elif containerCount == 2:
		for i in range(0, 2):
			data.append([])
		count = 0
		for td in tds:
			if count == 0:
				data[0].append(td)
			elif count == 1:
				data[1].append(td)
			count = count + 1
			if count > 1:
				count = 0

	elif containerCount == 1:
		data.append([])
		for td in tds:
			data[0].append(td)

	elif containerCount == 0:
		data = None

	return data

def parseHTML(html):
	"""
	Parse the 'html' passed in.

	This subroutine uses the open source module 'BeautifulSoup' to parse the
	HTML data.
	The algorithm involved is specific to a certain time period and is not
	applicable to other time periods. If the HTML changes, this will break.
	"""

	soup = bs4.BeautifulSoup(html, 'html.parser')

	tds = soup.findAll('td', { "class": lambda x:
		x and (x == "menugridcell" or x == "menugridcell_last" or x == "menulocheader") })

	data = buildDataContainer(tds)
	if data == None:
		return None

	restaurants = []
	for index, values in enumerate(data):
		restaurant = { restaurantName: "", restaurantKitchens: [] }
		for d in values:
			# separate the "restaurant name" from the "kitchens"
			for child in d.children:
				if type(child) is bs4.element.Tag:
					childclass = child.get('class')
					if (childclass != None and len(childclass) != 0 and childclass[0] == 'menuloclink'):
						line = child.text.replace(u'\xa0', u'')
						line = line.replace('*', '')
						# print()
						# print('RESTAURANT: ' + line)
						restaurant[restaurantName] = line
					else:
						# separate the kitchen name from the entrees
						kitchen = { kitchenName: "", kitchenItems: [] }
						for item in child:
							if type(item) is bs4.element.Tag:
								itemclass = item.get('class')
								if itemclass != None and len(itemclass) != 0 and ('category' in itemclass[0]):
									line = item.text.replace(u'\xa0', u'')
									line = line.replace('*', '')
									# print()
									# print('Kitchen: ' + line)
									kitchen[kitchenName] = line
								elif itemclass != None and len(itemclass) != 0 and ('level' in itemclass[0]):
									line = item.text.replace(u'\xa0', u'')
									line = line.replace('*', '')
									#print('e: ' + line)
									kitchen[kitchenItems].append(line)
						# print(kitchen)
						if kitchen[kitchenName] != "" and len(kitchen[kitchenItems]) != 0:
							restaurant[restaurantKitchens].append(kitchen)
		if restaurant[restaurantName] != "" and len(restaurant[restaurantKitchens]) != 0:
			restaurants.append(restaurant)
	# print(restaurants)

	return restaurants

import datetime

def buildURL(date, meal):
	"""
	Build URL from 'date' and 'meal'.

	Builds a url for the parser to get the menu data.
	The url depends on the 'Meal' (either breakfast, lunch, or dinner)
	and the data for which the menu is supposed be for.
	"""

	base = "http://menu.ha.ucla.edu/foodpro/default.asp?"
	meal = meal
	dateString = date.strftime('%m/%d/%Y')
	params = {'date': dateString, 'meal': meal.value, 'threshold': "2"}
	url = base + urlencode(params)
	return url


dateTime = datetime.date(2016, 6, 26)
# dateTime = datetime.date.today()
url = buildURL(dateTime, Meal.dinner)
print(url)

import json

import urllib.request
with urllib.request.urlopen(url) as response:
	html = response.read()
	restaurants = parseHTML(html)
	print(json.dumps(restaurants, indent=2))

