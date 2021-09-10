import pandas as pd
import sqlite3
from matplotlib import pyplot as plt

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
