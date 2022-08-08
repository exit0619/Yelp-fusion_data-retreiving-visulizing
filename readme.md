### Yelp Fusion - Finding the top restaurants in the world's richest cities.

**Yelp Fusion API**

The Yelp Fusion API allows you to get the best local content and user reviews from millions of businesses across 32 countries. This tutorial provides an overview of the capabilities our suite of APIs offered, provides instructions for how to authenticate API calls, and walks through a simple scenario using the API.

**Case Study**

I am a guy who likes to travel and explore local famous restaurants. So I want to find out, in the top 5 world richest cities, what restaurant categories are people's favorite on Yelp. 

**Data Sources**

Restaurants information: [Yelp Business Search](https://www.yelp.com/developers/documentation/v3/business_search) 
Yelp Business Search allows you to use different criteria, such as term, location, and so on, to search business information. The maximum number of information returns per search is 50. Therefore, here we analyze the top 49 restaurants from each city. The rating sort uses Yelp's rule: rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a Bayesian average. This is to prevent skewing results to businesses with a single review.

The 150 richest cities in the world by GDP in 2020: [City Mayors](http://www.citymayors.com/statistics/richest-cities-2020.html)
This case study is not interested in the ranking or the criteria to rank the richest cities in the world, but in the restaurants. Here the top 5 richest cities are Tokyo, New York, Los Angeles, London, and Chicago. 

**Data Retrieving**

We started with connecting to Yelp API.
```python
import requests
import json
import sqlite3

api_key = 'your API key'
headers = {'Authorization': 'Bearer %s' % api_key}

url = 'https://api.yelp.com/v3/businesses/search'
```
Setting the search inputs.
```python
term = input('Term: ')
location = input('Location: ')

params = {'term':term,'location':location,'sort_by':'rating','limit':50}

req = requests.get(url, params=params, headers=headers)
```
We want to input the data into sqlite database.
```python
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Businesses
    (id INTEGER UNIQUE, Name TEXT, Country TEXT, City TEXT, Category TEXT, Rating TEXT,
     Address TEXT)''')
```
All set. Then we can parse the json code to retrieve the information we need here, and insert into the table in the database.
```python
parsed = json.loads(req.text)

businesses = parsed["businesses"]

many = 0
start = None
cur.execute('SELECT max(id) FROM Businesses' )
row = cur.fetchone()
start = row[0]
if start is None : start = 0
for business in businesses:
    if ( many < 1 ) :
        conn.commit()
        sval = input('How many retrieves: ')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    name = business["name"]
    category = business["categories"][0]["alias"]
    country = business["location"]["country"]
    city = location
    rating = business["rating"]
    address = " ".join(business["location"]["display_address"])
    phone = business["phone"]
    start = start + 1
    cur.execute('''INSERT OR IGNORE INTO Businesses (id, Country, City, Name, Category, Rating, Address)
        VALUES ( ?, ?, ?, ?, ?, ?, ? )''', ( start, country, city, name, category, rating, address))
    print(country, ",", city, ",", name, ",", category, ",", rating)
    many = many - 1
```

**Data Visualizing**

Here we use import the library pandas to communicate with sqlite, matplitlib to draw the charts.
```python
import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
```
Connect to the database, and create dataframes for plotting.

First we want to find the top 5 most popular categoties among these five cities. 
```python
con = sqlite3.connect("content.sqlite")

restaurants_df = pd.read_sql_query("""SELECT DISTINCT category, COUNT(*) as Number
FROM Businesses
GROUP BY category
ORDER BY Number DESC
LIMIT 5""", con)

plt.bar(restaurants_df.Category, restaurants_df.Number)
plt.title("Top 5 MOST POPULAR RESTAURANT CATEGORIES")
plt.xlabel("Restaurant Category")
plt.ylabel("Number of Restaurants")
```
![Bar Chart](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Top5res.png?raw=true)

And then we go a little bit closer to see the percentage of the top 5 catogories in each country, using a pie chart.

```python
restaurants_df = pd.read_sql_query("""SELECT city, category, COUNT(*) AS Number
FROM Businesses
GROUP BY city, category
HAVING city = "Chicago"
ORDER BY city, Number DESC
LIMIT 5""", con)

labels = restaurants_df.Category
sizes = restaurants_df.Number
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        startangle=90)
ax1.axis('equal')
plt.title("5 Higherst Rated Restaurants Categories in Chicago")

restaurants_df = pd.read_sql_query("""SELECT city, category, COUNT(*) AS Number
FROM Businesses
GROUP BY city, category
HAVING city = "New York City"
ORDER BY city, Number DESC
LIMIT 5""", con)

labels = restaurants_df.Category
sizes = restaurants_df.Number
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        startangle=90)
ax1.axis('equal')
plt.title("5 Higherst Rated Restaurants Categories in New York City")

restaurants_df = pd.read_sql_query("""SELECT city, category, COUNT(*) AS Number
FROM Businesses
GROUP BY city, category
HAVING city = "London"
ORDER BY city, Number DESC
LIMIT 5""", con)

labels = restaurants_df.Category
sizes = restaurants_df.Number
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        startangle=90)
ax1.axis('equal')
plt.title("5 Higherst Rated Restaurants Categories in London")

restaurants_df = pd.read_sql_query("""SELECT city, category, COUNT(*) AS Number
FROM Businesses
GROUP BY city, category
HAVING city = "Tokyo"
ORDER BY city, Number DESC
LIMIT 5""", con)

labels = restaurants_df.Category
sizes = restaurants_df.Number
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        startangle=90)
ax1.axis('equal')
plt.title("5 Higherst Rated Restaurants Categories in Tokyo")

restaurants_df = pd.read_sql_query("""SELECT city, category, COUNT(*) AS Number
FROM Businesses
GROUP BY city, category
HAVING city = "Los Angeles"
ORDER BY city, Number DESC
LIMIT 5""", con)

labels = restaurants_df.Category
sizes = restaurants_df.Number
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        startangle=90)
ax1.axis('equal')
plt.title("5 Higherst Rated Restaurants Categories in Los Angeles")

plt.show()
```
![Pie Tokyo](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Pie_Tokyo.png?raw=true)
![Pie NYC](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Pei_NYC.png?raw=true)
![Pie LA](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Pie_LA.png?raw=true)
![Pie London](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Pie_London.png?raw=true)
![Pie Chicago](https://github.com/exit0619/Yelp-fusion_data-retrieving-visualizing/blob/main/Pie_Chicago.png?raw=true)
