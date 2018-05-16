from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('quadratic.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    print(user_data)
    genre, budget, rating = user_data['genre'], user_data['budget'], user_data['rating']
    root_1 = _solve_quadratic(genre, budget, rating)
    return jsonify({'root_1': root_1})


def _solve_quadratic(a, b, c):
    log_b = np.log(b)
    return f'You want to make a prediction of a movie:\
            <p> in the <b>{a}</b> Genre,\
            <p> with an MPAA Rating of <b>{c}</b>,\
            <p> with a budget of <b>{b}</b> and a\
            <p> log_budget of <b>{log_b}</b>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
