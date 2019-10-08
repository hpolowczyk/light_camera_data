#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests

import pandas as pd

from splinter import Browser

import pymongo

def scrape():


    # URL to the page with movies that grosses > $50M
    url = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m50&sort=opengross&p=.htm&order=DESC'

    #Scrape data on the page
    tables = pd.read_html(url)

    #Tables is a list of all the tables on the page, the required dataframe is stored in index 3
    df = tables[3]

    df.columns = ['Rank', 'Title', 'Studio', 'Opening', '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']

    #Remove heading row that's saved as the first row
    df = df.iloc[1:]

    df.set_index('Rank', inplace=True)

    df.head()


    # In[3]:


    # Tab -  $40 - 50M, has the remaining data
    url2 = 'https://www.boxofficemojo.com/alltime/weekends/?pagenum=m4050&sort=opengross&p=.htm&order=DESC'

    tables2 = pd.read_html(url2)

    #Tables is a list of all the tables on the page, the required dataframe is stored in index 3
    df2 = tables2[3]

    df2.columns = ['Rank', 'Title', 'Studio', 'Opening', '% of Total', 'Theaters', 'Average', 'Total Gross', 'Date']

    #Remove heading row that's saved as the first row
    df2 = df2.iloc[1:]

    df2.set_index('Rank', inplace=True)


    df2.head()


    # In[4]:


    #Concatenate the 2 dataframes
    boxOffice_df = pd.concat([df,df2])

    #We only need the top 250
    boxOffice_df = boxOffice_df.iloc[0:250]

    boxOffice_df.head()


    # In[5]:


    #Replace abbreviated studio names with actual Studio names
    print(boxOffice_df['Studio'].unique())

    boxOffice_df['Studio'].replace(['BV', 'Uni.', 'WB', 'LGF' ,'Sony', 'Sum.' ,'LG/S', 'Fox' ,'Par.', 'WB (NL)', 'P/DW' ,'DW', 'NM' ,'NL', 'MGM'], ['Buena Vista', 'Universal', 'Warner Bros.', 'Lionsgate' ,'Sony / Columbia', 'Summit Entertainment' ,'Lionsgate' , '20th Century Fox' ,'Paramount', 'Warner Bros.', 'Paramount' ,'Dreamworks SKG', 'Newmarket' ,'New Line', 'MGM'], inplace=True)


    # In[6]:


    boxOffice_df.head()


    # In[10]:


    boxOffice_df.head()


    # ## Export data to the DB

    # In[12]:


    #Establish a connection to the DB
    conn = 'mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority'
    client = pymongo.MongoClient(conn)


    # In[13]:


    # Declare the database
    db = client.db

    # Declare the collection
    collection = db.box_office


    # In[14]:


    collection.drop() # Drops collection if it already exists, to remove duplicates

    collection.insert_many(boxOffice_df.to_dict('records'))


    # ## Retrieve Movie URLs

    # In[ ]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[ ]:


    # Retrieve page with the requests module
    browser.visit(url)


    # In[ ]:


    # Create BeautifulSoup object
    soup = bs(browser.html,'html.parser')

    #Retrieve the required table
    movieTable = soup.find_all("table")[4]


    # In[ ]:



    eachMovie = movieTable.find_all("tr")

    movieList = []

    for one in range(len(eachMovie)):
        movieURL = eachMovie[one].find_all("td")[1].find("a")["href"]
        movieName = eachMovie[one].find_all("td")[1].text
        movieRank = eachMovie[one].find_all("td")[0].text
        
        movieList.append({"movieURL" : "https://www.boxofficemojo.com" + movieURL, "movieName" : movieName, "movieRank": movieRank})
        
        #print(f"movieURL: {movieLink}, movieName: {movieName}, movieRank: {movieRank}")
        
    movieList_df = pd.DataFrame( movieList)

    movieList_df = movieList_df.iloc[1:250]


    movieList_df#.head(15)


    # In[ ]:


    #Second tab

    # Retrieve page with the requests module
    browser.visit(url2)


    # In[ ]:


    # Create BeautifulSoup object
    soup = bs(browser.html,'html.parser')
        
    #Retrieve the required table
    movieTable2 = soup.find_all("table")[4]


    # In[ ]:



    eachMovie2 = movieTable2.find_all("tr")

    movieList2 = []

    for one in range(len(eachMovie2)):
        movieURL = eachMovie2[one].find_all("td")[1].find("a")["href"]
        movieName = eachMovie2[one].find_all("td")[1].text
        movieRank = eachMovie2[one].find_all("td")[0].text
        
        movieList2.append({"movieURL" : "https://www.boxofficemojo.com" + movieURL, "movieName" : movieName, "movieRank": movieRank})
        
        #print(f"movieURL: {movieLink}, movieName: {movieName}, movieRank: {movieRank}")
        
    movieList_df2 = pd.DataFrame( movieList2)

    movieList_df2 = movieList_df2.iloc[1:3]


    movieList_df2.head()


    # In[ ]:


    #Concatenate the 2 dataframes
    movieList_df = pd.concat([movieList_df,movieList_df2])

    movieList_df.head()


    # In[ ]:



    movieList_df.set_index('movieRank', inplace=True)

    movieList_df

