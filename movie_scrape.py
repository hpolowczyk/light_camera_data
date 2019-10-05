#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies
from bs4 import BeautifulSoup
import requests

import pandas as pd


# In[ ]:





# In[ ]:





# In[3]:


# $50M+
url = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m50&sort=opengross&p=.htm&order=DESC'


# In[ ]:





# In[4]:


tables = pd.read_html(url)

#Tables is a list of all the tables on the page, the required dataframe is stored in index 3
df = tables[3]

df.columns = ['Rank', 'Title', 'Studio', 'Opening', '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']

#Clean up title that's an extra row
df = df.iloc[1:]

#df.set_index('Rank', inplace=True)

df.head()


# In[5]:


# Tab -  $40 - 50M, has the remaining data
url2 = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m4050&sort=opengross&p=.htm&order=DESC'

tables2 = pd.read_html(url2)

#Tables is a list of all the tables on the page, the required dataframe is stored in index 3
df2 = tables2[3]

df2.columns = ['Rank', 'Title', 'Studio', 'Opening', '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']

#Clean up title that's an extra row
df2 = df2.iloc[1:]

#df2.set_index('Rank', inplace=True)

#Replace abbreviated studio names with actual Studio names
#print(df['Studio'].unique())

#df2['Studio'].replace(['BV', 'Uni.', 'WB', 'LGF' ,'Sony', 'Sum.' ,'LG/S', 'Fox' ,'Par.', 'WB (NL)', 'P/DW' ,'DW', 'NM' ,'NL', 'MGM'], ['Buena Vista', 'Universal', 'Warner Bros.', 'Lionsgate' ,'Sony / Columbia', 'Summit Entertainment' ,'Lionsgate' , '20th Century Fox' ,'Paramount', 'Warner Bros.', 'Paramount' ,'Dreamworks SKG', 'Newmarket' ,'New Line', 'MGM'], inplace=True)


df2.head()


# In[6]:



boxOffice_df = pd.concat([df,df2])
boxOffice_df = boxOffice_df.iloc[0:250]
boxOffice_df.head()


# In[7]:


#Replace abbreviated studio names with actual Studio names
print(boxOffice_df['Studio'].unique())

boxOffice_df['Studio'].replace(['BV', 'Uni.', 'WB', 'LGF' ,'Sony', 'Sum.' ,'LG/S', 'Fox' ,'Par.', 'WB (NL)', 'P/DW' ,'DW', 'NM' ,'NL', 'MGM'], ['Buena Vista', 'Universal', 'Warner Bros.', 'Lionsgate' ,'Sony / Columbia', 'Summit Entertainment' ,'Lionsgate' , '20th Century Fox' ,'Paramount', 'Warner Bros.', 'Paramount' ,'Dreamworks SKG', 'Newmarket' ,'New Line', 'MGM'], inplace=True)


# In[8]:


boxOffice_df.head()


# In[32]:


# Dependencies
import requests
import pymongo

# API URL
url = "http://www.omdbapi.com/?apikey=57e34fb6&plot=full"
# MongoDB connection
conn = 'mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority'
client = pymongo.MongoClient(conn)


# In[59]:


movie_data = []
wrong_movies= {"MIB 3":'tt1409024',
           "Fast & Furious Presents: Hobbs & Shaw":'tt6806448',
           "Star Wars: The Force Awakens": 'tt2488496',
           "Marvel's The Avengers":'tt0848228',
           "The Divergent Series: Insurgent":'tt2908446',
           "Dr. Seuss' The Lorax":'tt1482459',
           "Monsters Vs. Aliens":'tt0892782',
           "Jackass 3-D":'tt1116184',
           "Dr. Seuss' The Grinch (2018)":'tt2709692',
           "Fantastic Four: Rise of the Silver Surfer":'tt0486576'}

for title in boxOffice_df['Title']:
    if title in wrong_movies:
        movie_id = wrong_movies[title]
        movie = requests.get(url + '&i=' + movie_id).json()
        if movie['Response'] == "True":
            movie_data.append(movie)
    elif "(" in title:
        year = title[-5:][:-1]
        title = title[:-6]
        movie = requests.get(url + '&t=' + title + '&y=' + year).json()
        if movie['Response'] == "True":
            movie_data.append(movie)
    else:
        movie = requests.get(url + '&t=' + title).json()
        if movie['Response'] == "True":
            movie_data.append(movie)


# In[60]:


rotten_tomatoes = []
count = 0

for movie in movie_data:
    try:
        rating = movie['Ratings'][1]['Value']
        rotten_tomatoes.append(rating)
    except IndexError:
        rating = 'N/A'
        rotten_tomatoes.append(rating)


# In[74]:


movie_df = pd.DataFrame(movie_data)
movie_df['Rotten Tomatoes'] = rotten_tomatoes
movie_df.columns
movie_df = movie_df.reset_index()
movie_df['Rank'] = movie_df['index'] + 1


# In[62]:


boxOffice_df.dtypes
boxOffice_df["Rank"] = pd.to_numeric(boxOffice_df["Rank"])
boxOffice_df.dtypes


# In[75]:


df = movie_df[['Rank','Title','Plot','Actors', 'Director', 'Genre', 'Poster', 
               'Rated', 'imdbRating', 'Metascore','Rotten Tomatoes']]


# In[76]:


split_columns = ['Actors','Director','Genre']


split_actors = []
split_directors = []
split_genre = []
split_plot = []

for column in split_columns:
    for row in df[column]:
        split_row = row.split(", ")
        if column == 'Actors':
            split_actors.append(split_row)
        elif column == 'Director':
            split_directors.append(split_row)
        else:
            split_genre.append(split_row)


for row in df['Plot']:
    split_row = row.split(" ")
    split_plot.append(split_row)

split_df = df.copy()
split_df['Actors'] = split_actors
split_df['Director'] = split_directors
split_df['Genre'] = split_genre
split_df['Plot'] = split_plot


# In[ ]:





# In[77]:


new_df = boxOffice_df.merge(split_df,left_on = 'Rank',right_on='Rank')


# In[78]:


new_df = new_df[['Rank', 'Title_x', 'Studio', 'Opening', '% of Total', 'Theaters',
       'Average', 'Total Gross', 'Date', 'Plot', 'Actors',
       'Director', 'Genre', 'Poster', 'Rated', 'imdbRating', 'Metascore','Rotten Tomatoes']]

new_df = new_df.rename(columns={"Title_x": "Title"})


# In[79]:


new_df.head()


# In[80]:


movies_dict = new_df.to_dict('records')


# In[65]:


# Dependencies


# In[67]:


# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/


# In[81]:


# Declare the collection
collection = client.movie_db.movie_detail

collection.insert_many(movies_dict)

print('Data Uploaded')

