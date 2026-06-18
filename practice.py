import requests
import sqlalchemy as db
import pandas as pd

url = 'https://api.artic.edu/api/v1/artworks'
engine = db.create_engine('sqlite:///art.db')
response = requests.get(url)
print(response.status_code)
artworks_request = response.json()


works = artworks_request['data']
works_dict = {}

ind = 0
for w in works:
  works_dict[ind] = [w['id'], w['title']]
  ind+=1


worksDF = pd.DataFrame.from_dict(works_dict, orient='index', columns=["museum_id", "artwork_title"])
worksDF.to_sql('artwork', con=engine, if_exists='replace', index=False)

with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM artwork;")).fetchall()
   print(pd.DataFrame(query_result))
'''
current output:
200
    museum_id                        artwork_title
0         277                 Kantharos (Wine Cup)
1         255                           Fish Plate
2         183                 Kantharos (Wine Cup)
3         164          Column-Krater (Mixing Bowl)
4       60561                               Bureau
5      116399                          Boy's Armor
6       99766         Untitled (Butterfly Habitat)
7       69454                             Bedcover
8       76776  Kyoto Evergreen (Furnishing Fabric)
9       71562                             Sunlight
10      30659                           Breakwater
11      18856                             Fountain

YAYYY
'''

# art_id = w['id']
# art_title = w['title']
# art_url = https://www.artic.edu/artworks/{art_id}/{art_title}

