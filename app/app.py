from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.externals import joblib


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    '''
    Grabs the user inputs from json format and converts them to python variables
    Makes a prediction on those variables

    Parameters
    ----------
    None

    Returns
    -------
    json-ified version of the prediction statement
    '''
    user_data = request.json

    budget = user_data['budget']
    franchise = user_data['franchise']
    rating = user_data['rating']
    genre = user_data['genre']
    prod_method = user_data['prod_method']
    creative_type = user_data['creative_type']
    source = user_data['source']
    month = user_data['month']

    single_pred_test_2 = create_prediction_array(budget, franchise, rating, genre, prod_method, creative_type, source, month)
    prediction = np.exp(model.predict(single_pred_test_2))
    root_1 = print_prediction(prediction)
    print(user_data)
    # print(model_columns)
    # print(single_pred_test_2)
    # print(prediction)
    return jsonify({'root_1': root_1})

def print_prediction(prediction):
    '''
    Formats the prediction value into a currency format and converts it to
    html code format to print to the webpage

    Parameters
    ----------
    prediction in float format

    Returns
    -------
    html code to print the prediction
    '''
    prediction_str = '${:,.0f}'.format(prediction[0])
    return f'<p> Your prediction is: ' + prediction_str

def create_prediction_array(budget, franchise, rating, genre, prod_method, creative_type, source, month):
    '''
    Creates a prediction array to be called upon to make a prediction.
    Default array is defined below as df_single_pred (filled with mostly zeros).
    Converts user input variables to 1's for each input

    Parameters
    ----------
    The column titles that the user specified (eg. Genre: Action,
    Source: Original Screenplay, Month: June)

    Returns
    -------
    A 2d pandas df (although it is only a single row) with the correct user defined
    prediction variables
    '''
    df_single_pred = pd.DataFrame(np.array([[ 15.,   90.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.]]))
    df_single_pred.columns = model_columns

    df_single_pred.loc[0]['log_budget'] = np.log(budget)

    franchise_value = df_single_pred.loc[0]['is_franchise']
    if franchise == 'is_franchise':
        franchise_value = 1
    df_single_pred.loc[0]['is_franchise'] = franchise_value

    df_single_pred.loc[0][rating] = 1

    df_single_pred.loc[0][genre] = 1

    df_single_pred.loc[0][prod_method] = 1

    df_single_pred.loc[0][creative_type] = 1

    df_single_pred.loc[0][source] = 1

    df_single_pred.loc[0][month] = 1

    print(df_single_pred)
    
    return df_single_pred

if __name__ == '__main__':
    model = joblib.load('../model.pkl')
    model_columns = joblib.load('../model_columns.pkl')
    app.run(host='0.0.0.0', threaded=True)
