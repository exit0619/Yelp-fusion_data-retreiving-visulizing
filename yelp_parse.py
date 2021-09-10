import requests
import json
import sqlite3

api_key = 'wa3fd_QzLrL5ircAwtYoZi3y4Zia1J29ZVK9mOL-01jtzfIdCPhDnl4DlLc-9fMO0PukDqZ32Ctuzb7SH775b2y5lb4gf3OfNFgosYnVNcgVuuUvrGVgTCQi2z4vYXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

url = 'https://api.yelp.com/v3/businesses/search'

term = input('Term: ')
location = input('Location: ')

params = {'term':term,'location':location,'sort_by':'rating','limit':50}

req = requests.get(url, params=params, headers=headers)

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Businesses
    (id INTEGER UNIQUE, Name TEXT, Country TEXT, City TEXT, Category TEXT, Rating TEXT,
     Address TEXT)''')

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
