
#----------also works
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import json
from miniparse import officialticker
import sqlite3
import itertools
import time
#----------------SQL database
conn = sqlite3.connect('Losers.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Losers;
DROP TABLE IF EXISTS Ticker;
DROP TABLE IF EXISTS Incomechange;

CREATE TABLE Ticker (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    ticker TEXT UNIQUE
);

CREATE TABLE Incomechange (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    incomechange REAL
);

CREATE TABLE Losers (
    ticker_id       INTEGER,
    incomechange_id INTEGER,
    PRIMARY KEY (ticker_id, incomechange_id)
);
''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
x=0
tickers=list()
income=list()
for symbol in officialticker:
    try:
        basiceurl ='https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='
        additionalurl="&apikey=DDL7PYN9PTL8TNEW"
        ticker=symbol
        completeurl='https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ticker+additionalurl
        html = urllib.request.urlopen(completeurl,context=ctx)
        js = json.load(html)
        #not loads because it is not a string
        #js is a dictionary
        count=0
        sum=0
        actualincome=list()
        quarter=js["quarterlyReports"]
        #js is a dictionary with a list inside
        for twoquarters in quarter:
        #inside list
            count=count+1
            if count==3:
                break
            else:
                netincome=twoquarters["netIncome"]
                actualincome.append(int(netincome))
        percentincome=((actualincome[1]-actualincome[0])/(actualincome[0]))*100
        percentincome="{:.2f} %".format(percentincome)
        #2 decimals and percent
        tickers.append(symbol)
        income.append(percentincome)
        print(symbol,percentincome)
        x=x+1
        if x==5:
            break
        else:
            pass
    except:
        print("Not US stock")
ticker_idlist=list()
for ticker in tickers:
    cur.execute('''INSERT OR IGNORE INTO Ticker (ticker)
            VALUES ( ? )''', ( ticker, ) )
    cur.execute('SELECT id FROM Ticker WHERE ticker = ? ', (ticker, ))
    ticker_id = cur.fetchone()[0]
    ticker_idlist.append(ticker_id)
income_idlist=list()
for incomechange in income:
    cur.execute('''INSERT OR IGNORE INTO Incomechange (incomechange)
            VALUES ( ? )''', ( incomechange, ) )
    cur.execute('SELECT id FROM Incomechange WHERE incomechange = ? ', (incomechange, ))
    incomechange_id = cur.fetchone()[0]
    income_idlist.append(incomechange_id)

for (ticker_id, incomechange_id) in zip(ticker_idlist, income_idlist):
    cur.execute('''INSERT OR REPLACE INTO Losers
        (ticker_id, incomechange_id ) VALUES ( ?, ?)''',
        ( ticker_id, incomechange_id ) )
conn.commit()
# import the time module
print("Please wait one minute so that the API allows us to use the data")
# define the countdown func.
def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
        #calculates the number of minutes and seconds by mins being the quotient and secs being remainder
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
        #makes it wait for one second
		t -= 1
	print('You may run the code again')
# function call
countdown(60)
#html = urllib.request.urlopen(serviceurl,context=ctx)
#js = json.load(html)
#not loads because it is not a string
#js is a dictionary
# quarter=js["quarterlyReports"]
# for twoquarters in quarter:
    # count=count+1
    # if count==3:
        # break
    # else:
        # netincome=twoquarters["netIncome"]
        # actualincome.append(int(netincome))
# percentincome=((actualincome[1]-actualincome[0])/(actualincome[0]))*100
# percentincome="{:.2f}".format(percentincome)
#------------------already works-----------------
# API key is DDL7PYN9PTL8TNEW
# import requests
# import json
#replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=DDL7PYN9PTL8TNEW'
# r = requests.get(url)
# data = r.json()
 #js = json.loads(data) doesn't work as it is dictionary already
