# UCLA Parse

Web scrapper built with `BeautifulSoup` used for parsing UCLA data, including UCLA dining hall data.

This project is used as the backend for my iOS application Bruin Feed ([App Store](https://itunes.apple.com/us/app/bruin-feed/id993075117&mt=8), [Github](https://github.com/QingweiPeterLan/Bruin-Feed)).

**NOTE: This project has been only tested for Python 3**

## Features

* Parse dining hall menus from the UCLA website
* Parse nutrition data for specific entrees (with a specific ID)

# Usage

Copy the files `parse.py` and `nutrition.py` to your directory.

## Menu Parsing

### Command Line Interface (CLI)

The CLI for parsing dining hall menus is simple, simply run

```bash
$ python3 parse.py [year] [month] [day]
```

substituting values in the brackets. For example, if we wanted to parse the menus for Aug. 1, 2016, simply run

```bash
$ python3 parse.py 2016 8 1
```

There are other also options you can specify to custominze your parsing:

```
  -h, --help         shows the help message
  -n, --nutrition    determine whether to download nutrition data
  -b, --breakfast    download breakfast menus
  -l, --lunch        download lunch menus
  -d, --dinner       download dinner menus
```

The printed result will be a minified `JSON` string in the format

```python
{
    "b": [...],
    "l": [...],
    "d": [...]
}
```

### Using the `MenuParser` Class

A full example can be found in the file `run-menu.py`.

To use the `MenuParser` class, we would first include the following two lines

```python
from parse import Meal
from parse import MealParser
```

Then we create a `MenuParser` object with the arguments `date` (of type `datetime.datetime`), and `meal` (of type `Meal`). For example, we want to create a `MenuParser` with today's date for the meal dinner:

```python
import datetime

date = datetime.datetime.today()
meal = Meal.dinner
parser = MenuParser(date, meal)
```

Now we can parse the menus by calling `getMenus(shouldGetNutrition)`. The only argument is a `boolean` which specifies whether to download the nutrition data

```python
shouldGetNutrition = True      
menu = parser.getMenus(shouldGetNutrition)
```

This will return an array of dictionaries, each dictionary of the format

```python
kEntreeName = "e"
kType = "t"
kNutritionData = "n"

{
    kEntreeName: "...",
    kType: "...",
    kNutritionData: [...]
}
```

Note that `kNutritionData` consists of an array of nutrition data, elements of which will be explained below in the **Nutrition Parsing** section.

## Nutrition Parsing

### Command Line Interface (CLI)

To download the nutrition data for an entree with nutrition data of `ID` (**this `ID` can be found on the UCLA dining hall website, but you will have to look into the URL to locate it**) You would use it like this:

```bash
$ python3 nutrition.py [ID]
```

Suppose you want to download the nutrition data for an entree called **[Hungarian Beef Goulash](http://menu.ha.ucla.edu/foodpro/recipedetail.asp?RecipeNumber=075008)** (which has an `ID=075008`), we can use the CLI:

```bash
$ python3 nutrition.py 075008
```

The results will be an array of the format below (comments show which nutrition data each array element represents)

```python
[
  "0",   # total calories
  "0",   # calories from fat

  "0%",  # vitamin A
  "0%",  # vitamin C
  "0%",  # calcium
  "0%",  # iron

  "0g",  # total fat
  "0%",  # total fat percentage
  "0g",  # saturated fat
  "0%",  # saturated fat percentage
  "0g",  # trans fat

  "0mg", # cholesterol
  "0%",  # cholesterol percentage
  "0mg", # sodium
  "0%",  # sodium percentage

  "0g",  # total carbohydrate
  "0%",  # total carbohydrate percentage
  "0g",  # dietary fiber
  "0%",  # dietary fiber percentage
  "0g",  # sugars

  "0g"   # protein
]
```

### Using the `NutritionParser` Class

A full example can be found in the file `run-nutrition.py`.

To use the `NutritionParser` class, we would first include the following line

```python
from nutrition import NutritionParser
```

Then we create a `NutritionParser` object with the arguments `recipe` (of type `string`). For example, we want to create a `NutritionParser` with the recipe `ID=075008`:

```python
recipe = "075008"
parser = NutritionParser(recipe)
```

Now we can parse the nutrition data by calling `downloadNutritionData(shouldSave, filebase)`. Arguments include a `boolean` `shouldSave` which specifies whether to save the downloaded data as a file, and a `string` `filebase`, which specifies where to save the downloaded data (default is `./nutrition/`). For example, to download the data and not save, we use:

```python
nutrition = parser.downloadNutritionData()
```

To save the data in the default path, we use:

```python
shouldSave = True
nutrition = parser.downloadNutritionData(shouldSave)
```

To save to a specified location, such as `/home/user/desktop/nutrition/`, we use:

```python
shouldSave = True
filebase = "/home/user/desktop/"
nutrition = parser.downloadNutritionData(shouldSave, filebase)
```

The return value is a `JSON` object in the format described above.

# The MIT License (MIT)

Copyright (c) 2016 Qingwei Lan (qingweilandeveloper@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

