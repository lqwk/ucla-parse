# UCLA Parse

Web scrapper built with `BeautifulSoup` used for parsing UCLA data, including UCLA dining hall data.

This project is used as the backend for my iOS application Bruin Feed ([App Store](https://itunes.apple.com/us/app/bruin-feed/id993075117&mt=8), [Github](https://github.com/QingweiPeterLan/Bruin-Feed)).

**This project has been only tested for Python 3**

## Features

* Parse dining hall menus from the UCLA website
* Parse nutrition data for specific entrees (with a specific ID)

# Usage

Copy the files `parse.py` and `nutrition.py` to your directory.

## Command Line Interface (CLI)

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

The printed result will be a minified `JSON` string in the form

```json
{
    "b": [...],
    "l": [...],
    "d": [...]
}
```

## Using the `MenuParser` Class

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

This will return an array of dictionaries, each dictionary of the form

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

# The MIT License (MIT)

Copyright (c) 2016 Qingwei Lan (qingweilandeveloper@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

