import pandas as pd
import matplotlib.pyplot as plt
import math

def readTitles():
    movies = pd.read_csv('titles.csv')
    return movies

def readCast():
    cast = pd.read_csv('cast.csv.zip')
    return cast

def readReleaseDates():
    release_dates = pd.read_csv('release_dates.csv', parse_dates=['date'], infer_datetime_format=True)
    return release_dates

movies = readTitles()
cast = readCast()
release_dates = readReleaseDates()

def hasMoreThanX(rows, x):
    if len(rows)>x:
        return True
    return False
print("handle data") #make calls through debugger


