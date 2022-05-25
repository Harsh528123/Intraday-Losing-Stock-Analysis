# Loser Stock Analysis

I created a small program that gets the top 25 losers in the market for the day and retrieves their income change in the most recent quarter in a SQLite database. I used Beautiful Soup for web scraping the TradingView website for the top 25 loser stocks for the day and used Python to interact with my SQLite database. To obtain the income change in the most recent quarter, I used an AlphaVantage API to retrieve the JSON data and then parsed the data and send it to my SQLite database. Some things to note is that the AlphaVantage API works only for Canadian stocks while the top 25 loser stocks can be outside the Canadian market (TSX) which results in some empty information. Another thing to note is that AlphaVantage API has a limit of 5 API calls per minute, so I had to implment a one minute timer. 

## How to Install and Run Project 
  1. To run the project, first clone it. Please have the sqlite3, time, ssl, bs4, urllib.request, urllib.parse, urllib.error, datetime libraries installed along with the      latest version of Python. Also have SQLite installed. 
  2. In the terminal run python3 MainProgram.py. 
  3. Open the database on DB Browser SQLite under the name 'Losers.sqlite'. 
