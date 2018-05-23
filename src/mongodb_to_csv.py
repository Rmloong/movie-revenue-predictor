"""
This module takes the cleaned collection from
MongoDB and converts it to a pandas DataFrame
and writes it to a csv. Ultimately to be used
by model.py to fit and store the model. 
"""
import pickle
import numpy as np
import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import GridSearchCV
# from sklearn.externals import joblib
import pymongo

def create_ww(dataframe):
    dom = dataframe['Domestic Box Office'].fillna(0, inplace=False)
    intl = dataframe['International Box Office'].fillna(0, inplace=False)
    #nulls will be replaced with median budget $25mil
    budget_isna = dataframe['Production Budget'].isna()
    budget = dataframe['Production Budget'].fillna(25000000, inplace=False)

    runtime_isna = dataframe['Running Time'].isna()

    df = pd.DataFrame()

    dom_numeric = dom.apply(pd.to_numeric)
    intl_numeric = intl.apply(pd.to_numeric)

    df['ww_agg'] = dom_numeric + intl_numeric
    df['production_budget'] = budget.apply(pd.to_numeric)

    df['log_ww_agg'] = df['ww_agg'].apply(np.log)
    df['log_budget'] = df['production_budget'].apply(np.log)

    df['budget_isna'] = budget_isna
    df['runtime_isna'] = runtime_isna

    return df

def build_clean_dataset(dataframe):
    df = create_ww(dataframe)
    df['ratings'] = parse_mpaa_col(dataframe)
    df['runtime'] = parse_runtime_col(dataframe)
    df['is_franchise'] = create_franchise_dummy(dataframe)
    df['genre'] = parse_genre(dataframe)
    df['prod_method'] = parse_prod_method(dataframe)
    df['creative'] = parse_creative(dataframe)
    df['source'] = parse_source(dataframe)
    df['month'], df['day'], df['year'] = parse_release_date(dataframe)
    return df

def dummify_df(dataframe):
    df_dummies_ratings = pd.get_dummies(dataframe.ratings)
    df_dummies_genre = pd.get_dummies(dataframe.genre)
    df_dummies_prod_method = pd.get_dummies(dataframe.prod_method)
    df_dummies_creative = pd.get_dummies(dataframe.creative)
    df_dummies_source = pd.get_dummies(dataframe.source)
    df_dummies_month = pd.get_dummies(dataframe.month)

    df_with_dummies = dataframe[['log_ww_agg', 'log_budget', 'budget_isna','runtime', 'runtime_isna', 'is_franchise']]

    df_with_all_dummies = pd.concat([df_with_dummies, df_dummies_ratings,
                                    df_dummies_genre, df_dummies_prod_method,
                                    df_dummies_creative, df_dummies_source,
                                    df_dummies_month], axis =1)
    return df_with_all_dummies

def parse_mpaa_col(dataframe):
    ratings = dataframe.loc[:,'MPAA Rating']
    ratings = ratings.apply(lambda a: str(a))
    ratings = ratings.apply(lambda b: b.split()[0])
    ratings = ratings.apply(strip_text)
    return ratings

def strip_text(bad_text):
    if bad_text.endswith('(Rating'):
        bad_text = bad_text.replace('(Rating', '')
    return bad_text

def parse_runtime_col(dataframe):
    runtime = dataframe['Running Time']
    runtime = runtime.fillna(95.1) #<- This was the median of the non-null runtimes
    runtime = runtime.apply(lambda x: str(x))
    runtime = runtime.apply(lambda x: x.split()[0])
    runtime = runtime.apply(float)
    return runtime

def create_franchise_dummy(dataframe):
    franchise = dataframe['Franchise'].isna() ^ 1
    return franchise

def parse_genre(dataframe):
    genre = dataframe['Genre']
    return genre

def parse_prod_method(dataframe):
    prod_method = dataframe['Production Method']
    return prod_method

def parse_creative(dataframe):
    creative = dataframe['Creative Type']
    return creative

def parse_source(dataframe):
    source = dataframe['Source']
    return source

def parse_release_date(dataframe):
    months = []
    days = []
    years = []
    for date in dataframe['Domestic Releases']:
        if date == date: #checking if null. if true then not null
            month = list(date.split(' '))[0]
            day = list(date.split(' '))[1]
            year = list(date.split(' '))[2]
        else:
            month = None
            day = None
            year = None
        months.append(month)
        days.append(day)
        years.append(year)
    return months, days, years

if __name__ == '__main__':
    mc = pymongo.MongoClient()
    db = mc['movies_metadata']
    movies_clean_v2 = db['movies_clean_v2']
    df_clean = pd.DataFrame(list(movies_clean_v2.find()))
    df_clean_data = pd.DataFrame(list(df_clean['data']))
    df_ready_for_model = build_clean_dataset(df_clean_data)
    df_with_all_dummies = dummify_df(df_ready_for_model)
    df_with_all_dummies.to_csv('../data/data_cleaned.csv', sep='|', index_label = False)
