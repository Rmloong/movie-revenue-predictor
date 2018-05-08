from selenium import webdriver
import selenium
import time
import pymongo
import requests
from bs4 import BeautifulSoup
import time
import json

import numpy as np

def create_mongodb():
    mc = pymongo.MongoClient()  # Connect to the MongoDB server using default settings
    db = mc['movies_metadata']  # Use (or create) a database called 'movies_metadata
    movies = db['movies'] #Create a collection called movies

    #Webscrape and add each movie html data to the collection movies from the movies_metadata db
    browser = webdriver.Firefox()
    for i in range(2017,2001,-1)
        for j in range(474,600):
            browser.get("https://www.the-numbers.com/United-States/movies/year/"+str(i))
            #If the worldwide revenue is a nonzero amount... then go to the direct webpage for the movie
            #Then store that webpage's html code in the pymongo collection
            if (browser.find_element_by_css_selector("#page_filling_chart > center:nth-child(7) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(" + str(i) + ") > td:nth-child(5)").text != '$0'):
                url = browser.find_element_by_css_selector("#page_filling_chart > center:nth-child(7) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(" + str(i) + ") > td:nth-child(1) > b:nth-child(1) > a:nth-child(1)").get_attribute('href')
                DELAY = 0.2 + np.random.random() # time to wait between HTTP requests
                time.sleep(DELAY)  # pause between HTTP requests
                browser.get(url)
                html = browser.page_source
                movies.insert_one({'url': url,
                                 'ts': time.time(),
                                 'html': html
                                 })
                #print(i)
