import sqlite3
import ssl
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

''' 
This program is to get the required tickers so that it can be inputed into the alpha vantage api
'''
url = input('Enter link:')
if len(url)==1:
    url="https://www.tradingview.com/markets/stocks-usa/market-movers-losers/"
    
html = urllib.request.urlopen(url,context=ctx).read()
# ugly html
soup = BeautifulSoup(html, "html.parser")
rawlist=list()
for small_data in soup.find_all("a",{"class":"tv-screener__symbol"}):
    # searches for tags with specific class attribute 
    slink=small_data['href']
    #filters out content from attribute
    rawlist.append(slink)
tickerlist=rawlist[0::2]
#makes sure names only comes once and grabs the ticker symbol
officialticker=list()
for ticker in tickerlist:
    tlist=ticker.split("-")
    newticker=tlist[1].replace("/","")
    # cleans up for the official ticker symbol
    officialticker.append(newticker)
#print(officialticker)
