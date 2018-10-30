from flask_restplus import Resource
from flask import Flask,jsonify
from flask_restplus import Api
import os
import pandas as pd
from src.datamanipulation.airline_manipulation import transform_data

api = Api()
app = Flask(__name__)
api.init_app(app)

def get_flights_data():
    flights_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'flights.csv'))
    transformed = transform_data(flights_data)
    return transformed

@app.route('/top20col/<string:col_name>')
class TopColData(Resource):
    def get(self, col_name):
        return jsonify(get_flights_data()[col_name].head(20))

if __name__ == '__main__':
    app.run(debug=True)