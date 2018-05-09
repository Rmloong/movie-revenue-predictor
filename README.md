# movie-revenue-predictor

#May 8, 2018

# Problem Statement
The entertainment business is inherently an industry with quite a bit of risk. Each individual movie has budgets, essentially investments, that can exceed hundreds of millions of dollars. It is not a guarantee whether these investments will pay off. It would be beneficial for studios to be able to predict how much a movie will make in gross receipts based upon a variety of combination of obvious and non-obvious factors. They can then make better decisions on which projects to greenlight, and even perhaps limit (or scale up) the appropriate budget.

This model is intended to assist movie studios in making decisions on whether or not to move ahead with a certain movie. This is usually years before the movie even comes out. Other models might use additional data based upon data that can be gathered leading up to a movie’s release (trailer views, social media data, etc.) but that information would not be available to a studio who is making their decision before any of this happens.

# Website

www.the-numbers.com

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
Because of the nature of the problem, and taking the stance of a hypothetical
Hollywood studio exec, all productions are assumed to be American productions.
Therefore only data for American productions was collected. The webpage being
scraped has already been narrowed to show only US productions (or co-productions).

#Data Preparation

##Feature engineering

##

# Model

# Model Evaluation

# Conclusion
