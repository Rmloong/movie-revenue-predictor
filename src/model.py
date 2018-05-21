
"""
Module containing model fitting code for a web application that implements a
text classification model.
When run as a module, this will load a csv dataset, train a classification
model, and then pickle the resulting model object to disk.
"""
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import pymongo

def get_data(filename):
    """Load clean data from a file and return training data.
    Parameters
    ----------
    filename: The path to a csv file containing the cleaned data.

    Returns
    -------
    X: A numpy array containing the columns used for training.
    y: A numpy array containing log(rev) values for model response.
    """

    df = pd.read_csv(filename, sep = '|')
    X = df.iloc[:,1:]
    y = df.iloc[:,0]
    return X,y

def build_model(X,y):
    '''
    Builds a random forest model based upon the best parameters found in GridSearchCV
    Then pickles it (puts into storage)
    Parameters
    ----------
    X: A numpy array containing the columns used for training.
    y: A numpy array containing log(rev) values for model response.

    Returns
    -------
    None, the model will be pickled (put into storage)

    '''
    rf_best_params = RandomForestRegressor(n_estimators = 1000, max_depth = 10, max_features = 10)
    rf_best_params.fit(X,y)
    joblib.dump(rf_best_params, 'model.pkl')
    model_columns = X.columns
    joblib.dump(model_columns, 'model_columns.pkl')
    return None

if __name__ == '__main__':
    X, y = get_data('../data/data_cleaned.csv')
    build_model(X,y)
