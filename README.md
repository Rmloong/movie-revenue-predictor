# movie-revenue-predictor

#(Lasted updated) May 23, 2018

# Problem Statement
The entertainment business is inherently an industry with quite a bit of risk. Each individual movie has budgets, essentially investments, that can exceed hundreds of millions of dollars. It is not a guarantee whether these investments will pay off. It would be beneficial for studios to be able to predict how much a movie will make in gross receipts based upon a variety of combination of obvious and non-obvious factors. They can then make better decisions on which projects to greenlight, and even perhaps limit (or scale up) the appropriate budget.

This model is intended to assist movie studios in making decisions on whether or not to move ahead with a certain movie. This is usually years before the movie even comes out. Other models might use additional data based upon data that can be gathered leading up to a movie’s release (trailer views, social media data, etc.) but that information would not be available to a studio who is making their decision before any of this happens.

# Websraping

www.the-numbers.com - Ultimately I chose this website
because it had the single most complete data source
for movie data that I could find. Other websites
explored included BoxOfficeMojo and IMDB.

# Data Filtering

## Years
Only recent years are taken due to the following reasons:
  1. The older the data is, the less relevant it is. Certain actors/directors/producers may retire. Certain
  2. The time requirement for scraping multiple years is quite high

However, a single recent year of data is insufficient, so we have settled on
three for now (10 to 15 would be ideal but time to scrape is a constraint)

## Revenue > 0
Reasons;
  1. Because of the large range of possible revenue values, basically $0 to
    $3 billion, we will be fitting the model on log(revenue). logarithmic values of
    0 are mathematically impossible, so will eventually be excluded from the
    dataset anyway.
  2. Revenue of 0 usually means one of a few things, all of which are irrelevant
    to our problem:
    a. The data was unavailable.
    b. The movie went straight to home video release.

## Production Country
Because of the nature of the problem, and taking the stance of a hypothetical Hollywood studio exec, all productions are assumed to be American productions.
Therefore only data for American productions was collected. The webpage being scraped has already been narrowed to show only US productions (or co-productions).

#The Process

##Files within src directory
1. Webscraping - webscrape.py: Scrapes each individual movie page and stores the raw html code
into a MongoDB   
2. Convert raw HTML to cleaner version on MongoDB -
clean_mongodb.py: Converts the raw html code into a
better prepared format to be eventually converted to
a python pandas dataframe
3. Convert the new collection in MongoDB to a pandas
dataframe and writes it to a csv file.
4. Creates the model - model.py : Creates a Random Forest regression model and fits it on the data.
The cross validation and gridsearching was done within jupyter notebook reworked_models.ipynb. The
best model parameters are coded in model.py

##Files within app directory
Note: The code here will be able to recreate the
web app locally, but will not change the actual website www.predictmovierevenue.com as that code
is located on an AWS EC2 instance.

1. app.py & index.html - Allows the user the input
feature variables and outputs three things:
  1. Predicted movie revenue
  2. Lower Bound interval
  3. Upper Bound interval

Note on bounds: The bounds are based upon the range
of 60% of the decision tree predictions within the
Random Forest model. In other words, 60% of the predictions lied between those two values.

# Conclusion & Next Steps
The model had a general test MSE of 4.76, which was against a range of log(revenue) values between 0.01 and 22. This was not great and I surmise could be
improved upon greatly by (among other things):
1. Adding specific franchise dummy variables to capture the brand recognition of each franchise. (Star Wars, MCU, Harry Potter, etc.)
2. Providing some way to fill in null budget values
with similar values of similar movies (such as kNN)
3. Adding actor and director dummy variables. This data was scraped but due to time constraints was not included in the final model.
4. Add more years worth of data. The initial model
is fitted on data from 2015-2017.
