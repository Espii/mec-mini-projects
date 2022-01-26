import json
import os
import requests
from dotenv import load_dotenv  # if missing this module, simply run `pip install python-dotenv`

load_dotenv()
def makeRequest():
    API_KEY = os.getenv('NASDAQ_API_KEY')
    baseUrl="https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X.json"

    start_date="2017-01-01"
    end_date="2017-12-31"
    parameters="?start_date="+start_date+"&end_date="+end_date+"&api_key="+API_KEY
    url=baseUrl+parameters
    parameters={
        'api_key':API_KEY,
        'start_date':start_date,
        'end_date':end_date
    }
    response = requests.get(url, data=parameters)
    return response

def getColumnIndex(dataset, name):
    #can optimize using dicionary
    colNames=dataset["column_names"]
    for i in range(len(colNames)):
        if colNames[i]==name:
            return i
    return -1

def getMinMaxPrices(dataset, records, colName):
    openMin=records[0][getColumnIndex(dataset, colName)];
    openMax=records[0][getColumnIndex(dataset, colName)];
    counter=1
    while counter<len(records):
        i=counter
        counter=counter+1
        
        record = records[i]
        openPrice = record[getColumnIndex(dataset, colName)]
        if openPrice == None:
            continue
        if openPrice>openMax:
            openMax=openPrice
        if openPrice<openMin:
            openMin=openPrice
    return {
        'min':openMin,
        'max':openMax
    }

def getLargestChangeBetweenAnyTwoDays(dataset, records):
    close = getMinMaxPrices(dataset, records, "Close")
    return abs(close["max"]-close["min"])

def getLargestChange(dataset, records):
    largestChange = 0
    largestChangeIndex = -1
    counter=1
    for i in range(len(records)):
        record=records[i]
        high = record[getColumnIndex(dataset, "High")]
        low = record[getColumnIndex(dataset, "Low")]
        if (high == None or low == None):
            continue
        change = abs(high-low)
        if (change>largestChange):
            largestChange=change
            largestChangeIndex=i
    return {
        'change':largestChange,
        'index':largestChangeIndex
    }

def getAverageDailyTradingVolume(dataset, records):
    sum=0
    count=0
    for record in records:
        tVolume = record[getColumnIndex(dataset, "Traded Volume")]
        if (tVolume == None):
            continue
        count=count+1
        sum=sum+tVolume
    return sum/count

r = makeRequest();
#print(r.text) #python project.py > output.txt

rData = json.loads(r.text)
dataset = rData["dataset"]
records = dataset["data"]

# can put all the functions in a single loop to "optimize" but the difference would essentially just be O(4n) vs O(n)
# where n = number of records. Both are linear growth and can be reduced to O(n) so shouldn't be that significant.
q1 = r.text
q2 = rData
q3 = getMinMaxPrices(dataset, records, "Open")
q4 = getLargestChange(dataset, records)
q5 = getLargestChangeBetweenAnyTwoDays(dataset, records)
q6 = getAverageDailyTradingVolume(dataset, records)
print(q3)
print(q4)
print(q5)
print(q6)








