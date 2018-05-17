from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.externals import joblib


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('quadratic.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    print(user_data)
    budget = user_data['budget']
    franchise = user_data['franchise']
    rating = user_data['rating']
    genre = user_data['genre']
    prod_method = user_data['prod_method']
    creative_type = user_data['creative_type']
    source = user_data['source']
    month = user_data['month']

    root_1 = _solve_quadratic(budget, franchise, rating, genre)
    single_pred_test_2 = create_prediction_array(budget, franchise, rating, genre, prod_method, creative_type, source, month)
    prediction = np.exp(model.predict(single_pred_test_2))
    print(model_columns)
    print(single_pred_test_2)

    return jsonify({'root_1': root_1, 'prediction': list(prediction)})

def _solve_quadratic(budget, franchise, rating, genre):
    log_b = np.log(budget)
    return f'You want to make a prediction of a movie:\
            <p> in the <b>{genre}</b> Genre,\
            <p> with an MPAA Rating of <b>{rating}</b>,\
            <p> with a budget of <b>{budget}</b> and a\
            <p> log_budget of <b>{log_b}</b>'

def create_prediction_array(budget, franchise, rating, genre, prod_method, creative_type, source, month):
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

    return df_single_pred

if __name__ == '__main__':
    model = joblib.load('../model.pkl')
    model_columns = joblib.load('../model_columns.pkl')
    app.run(host='0.0.0.0', threaded=True)
