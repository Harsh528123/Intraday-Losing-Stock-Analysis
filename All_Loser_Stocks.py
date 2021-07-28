import sqlite3
import time
import ssl
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
from datetime import datetime, timedelta
from requests import get
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
import re
import bs4
import itertools


url = input('Enter link:')
if len(url)==1:
    url="https://www.tradingview.com/markets/stocks-usa/market-movers-losers/"
html = urllib.request.urlopen(url,context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
rawlist=list()
for small_data in soup.find_all("a",{"class":"tv-screener__symbol"}):
    slink=small_data['href']
    rawlist.append(slink)
tickerlist=rawlist[0::2]
officialticker=list()
for ticker in tickerlist:
    tlist=ticker.split("-")
    newticker=tlist[1].replace("/","")
    officialticker.append(newticker)
#print(officialticker)




    #slink is a string
    # slink=slink.replace("?","/profile?")
    # finallink="https://finance.yahoo.com"+ slink
    # linklist.append(finallink)
#-------------------------
# tickerlist=list()
# for link in linklist:
    #link is a string
    # ticker_s=link.split('/')
    # ticker=(ticker_s[4]).rstrip()
