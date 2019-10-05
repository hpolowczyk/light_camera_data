from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo

# API URL
url_api = 'http://www.omdbapi.com/?apikey=57e34fb6&plot=full'
# MongoDB connection
conn = 'mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/Scrape?retryWrites=true&w=majority'
client = pymongo.MongoClient(conn)

url_50M = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m50&sort=opengross&p=.htm&order=DESC'
url_40to50M = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m4050&sort=opengross&p=.htm&order=DESC'

# Convert tables using pandas
tables = pd.read_html(url_50M)
# Since tables is a list of all the tables on the page, the required dataframe is stored in index 3
df = tables[3]
# Select desired columns
df.columns = ['Rank', 'Title', 'Studio', 'Opening',
              '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']
# Clean up title that's an extra row
df = df.iloc[1:]

tables2 = pd.read_html(url_40to50M)
df2 = tables2[3]
df2.columns = ['Rank', 'Title', 'Studio', 'Opening',
               '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']
df2 = df2.iloc[1:]

# Combine the two tables
boxOffice_df = pd.concat([df, df2])
# Only select the first 251 rows (with first row being the column names)
boxOffice_df = boxOffice_df.iloc[0:250]
# Clean up studio names, replacing abbreviations with full name
boxOffice_df['Studio'].replace(['BV', 'Uni.', 'WB', 'LGF', 'Sony', 'Sum.', 'LG/S', 'Fox', 'Par.', 'WB (NL)', 'P/DW', 'DW', 'NM', 'NL', 'MGM'], ['Buena Vista', 'Universal', 'Warner Bros.', 'Lionsgate',
                               'Sony / Columbia', 'Summit Entertainment', 'Lionsgate', '20th Century Fox', 'Paramount', 'Warner Bros.', 'Paramount', 'Dreamworks SKG', 'Newmarket', 'New Line', 'MGM'], inplace=True)

movie_data = []
wrong_movies = {"MIB 3": 'tt1409024',
                   "Fast & Furious Presents: Hobbs & Shaw": 'tt6806448',
                    "Star Wars: The Force Awakens": 'tt2488496',
                    "Marvel's The Avengers": 'tt0848228',
                    "The Divergent Series: Insurgent": 'tt2908446',
                    "Dr. Seuss' The Lorax": 'tt1482459',
                    "Monsters Vs. Aliens": 'tt0892782',
                    "Jackass 3-D": 'tt1116184',
                    "Dr. Seuss' The Grinch (2018)": 'tt2709692',
                    "Fantastic Four: Rise of the Silver Surfer": 'tt0486576'}

for title in boxOffice_df['Title']:
    if title in wrong_movies:
        movie_id = wrong_movies[title]
        movie = requests.get(url_api + '&i=' + movie_id).json()
        if movie['Response'] == "True":
            movie_data.append(movie)
    elif "(" in title:
        year = title[-5:][:-1]
        title = title[:-6]
        movie = requests.get(url_api + '&t=' + title + '&y=' + year).json()
        if movie['Response'] == "True":
            movie_data.append(movie)
    else:
        movie = requests.get(url_api + '&t=' + title).json()
        if movie['Response'] == "True":
            movie_data.append(movie)

rotten_tomatoes = []
count = 0

for movie in movie_data:
    try:
        rating = movie['Ratings'][1]['Value']
        rotten_tomatoes.append(rating)
    except IndexError:
        rating = 'N/A'
        rotten_tomatoes.append(rating)

movie_df = pd.DataFrame(movie_data)
movie_df['Rotten Tomatoes'] = rotten_tomatoes
movie_df.columns
movie_df = movie_df.reset_index()
movie_df['Rank'] = movie_df['index'] + 1

new_df = movie_df[['Rank', 'Title', 'Plot', 'Actors', 'Director', 'Genre', 'Poster',
                       'Rated', 'imdbRating', 'Metascore', 'Rotten Tomatoes']]

merged_df = boxOffice_df.merge(df, left_on='Rank', right_on='Rank')

merged_df = merged_df[['Rank', 'Title_x', 'Studio', 'Opening', '% of Total', 'Theaters','Average', 'Total Gross', 'Date', 'Plot', 'Actors','Director', 'Genre', 'Poster', 'Rated', 'imdbRating', 'Metascore', 'Rotten Tomatoes']]
merged_df.rename(columns={"Title_x": "Title"})
movies_dict = merged_df.to_dict('records')

collection = client.db.trial
collection.insert_many(movies_dict)

print("Data uploaded!")