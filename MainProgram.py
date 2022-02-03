import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import json
from All_Loser_Stocks import officialticker
import sqlite3
import itertools
import time
#----------------SQL database
def SQL_database():
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

# countdown is used for the api call rate of 5 calls per minute
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

def ticker(tickers):
    ticker_idlist=list()
    for ticker in tickers:
        cur.execute('''INSERT OR IGNORE INTO Ticker (ticker) VALUES ( ? )''', ( ticker, ) )
        cur.execute('SELECT id FROM Ticker WHERE ticker = ? ', (ticker, ))
        ticker_id = cur.fetchone()[0]
        #gets the id numbers
        ticker_idlist.append(ticker_id)
    return(ticker_idlist)

def income(income):
    income_idlist=list()
    for incomechange in income:
        cur.execute('''INSERT OR IGNORE INTO Incomechange (incomechange)
        VALUES ( ? )''', ( incomechange, ) )
        cur.execute('SELECT id FROM Incomechange WHERE incomechange = ? ', (incomechange, ))
        # inserts values into SQLite database
        incomechange_id = cur.fetchone()[0]
        income_idlist.append(incomechange_id)
    return(income_idlist)

def SQL_ids(ticker_idlist,income_idlist):
    for (ticker_id, incomechange_id) in zip(ticker_idlist, income_idlist):
        cur.execute('''INSERT OR REPLACE INTO Losers (ticker_id, incomechange_id ) VALUES ( ?, ?)''',
        ( ticker_id, incomechange_id ) )
        # inserts id values into SQlite database
        conn.commit()

def fetchingdata(officialticker):
    tickers=list()
    income_c=list()
    actualincome=list()
    stopcallingAPI=0
    for symbol in officialticker:
        try:
            basiceurl ='https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='
            additionalurl="&apikey=DDL7PYN9PTL8TNEW"
            ticker=symbol
            completeurl='https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ticker+additionalurl
    	    # each ticker will be going through the api
            html = urllib.request.urlopen(completeurl,context=ctx)
            js = json.load(html)
    	    # able to parse the json data now
            #not loads because it is not a string
            #js is a dictionary
            count=0
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
            percentincome=((actualincome[1]-actualincome[0])/(actualincome[0]))*10
            # calculate percent income
            percentincome="{:.2f} %".format(percentincome)
            #2 decimals and percent
            tickers.append(symbol)
            income_c.append(percentincome)
            #print(symbol,percentincome)
            stopcallingAPI+=1
            if stopcallingAPI==5:
    	    # api limit is 5 calls a minute so we have to wait
    	    print("Please wait one minute so that the API allows us to use the data")
                countdown(60)
            else:
                pass
        except:
            print("Not US stock")
    return(tickers,income_c)
	# if it is not a US stock, alphavantage will not have data for it

def main():
    SQL_database()
    # opens a database
    tickers,income_c=fetchingdata(officialticker)
    #gets tickers and income
    ticker_idlist=ticker(tickers)
    income_idlist=income(income)
    #gets corresponding ids and puts ticker and income in the database
    SQL_ids(ticker_idlist,income_idlist)
    #inserts ids in table

if __name__=="__main__":
    main()
