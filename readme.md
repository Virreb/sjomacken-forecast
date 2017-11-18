# Sjomacken Forecast
Python3.6 is used in this project.

## Setup
To install modules, you need the python package manager pip (sudo apt-get install pip).

### Virtual environment
It is recommended to use a virtual environment to install packages in, so they don't get installed globally. There are many tools for this but the most used low-lever is called virtualenv.

> pip install virtualenv

Create a virtual environment for a project:

> cd my_project_folder && virtualenv env -p python3.6

This creates a copy of Python3.6 in whichever directory you ran the command in, placing it in a folder named 'env'. To begin using the virtual environment, it needs to be activated:

> source env/bin/activate

This will now show in the terminal prompt. To deactivate the venv, just use the command

> deactivate

In Pycharm, you can also choose the virtualenv to be the standard python interpreter.

### Packages
The easiest way to install the required packages is to read the requirements.txt file in the project root. Don't forget to activate your virtual environment first!

> pip install -r requirements.txt

If some package is added later on, you can simply create a new requirements.txt file with

> pip freeze > requirements.txt

You might need to install the tkinter package aswell:

> sudo apt-get install python3-tk

### Data
Data is stored in the folder 'data' and consists of five parts:
* kortautomat.csv: Revenue from the card machine for fuel, active the whole year.
* revenue.csv: Revenue from the store, only active during the summer.
* smhi-min-max-temp.csv: Daily max min temperatures
* smhi-regn.csv: Daily total rain data in millimeters.
* smhi-vind.csv: Mid-day wind speed and direction.

The SMHI data was taken from the nearest physical SMHI measurement station (not in Hunnebo).
One maybe should use the calculated values for Hunnebo instead from SMHI.

There's also 'data.json' file which has all of the above data combined as a dict with dates as keys.
One could look into using the 'pandas' package framework instead of dicts.

Good to know:
* The 'kajakuthyrning' started first in the summer of 2016.
* The 'skoteruthyrning' started first in the summer of 2017.
* The 'service' is very sparse.
* If no sales has been made on a date, the date is not appended.

Should have a break points for the above.

## Goals
Here follows a idea of what could be needed and useful:

* Given a range of dates (maybe weighted with weather-data), what will be the projected revenue of products?
The most important products are 'bensin' and 'diesel'. (Multivariate forecasting, or maybe kNN)
* What is the seasonality? (Tip: Facebook prophet)
* How much staff will be needed tomorrow and the day after tomorrow? (Where the weather forecasting is usually good)
It is the leasing of boats, kayaks and jet-skis that needs most time of the staff. So if all of these are active/high
one day, you need at least 2 persons. But of course, the other products takes time as well.
