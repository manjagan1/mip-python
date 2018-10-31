from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, abort, reqparse
import os
import pandas as pd
import json
import numpy as np
from src.datamanipulation.airline_manipulation import transform_data

app = Flask(__name__)
api = Api(app)
# api.init_app(app)

ns_flight = api.namespace("flights")
# ns_airline = api.namespace("airline")
api.add_namespace(ns_flight, path = '/flights')

def get_flights_data():
    flights_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'flights.csv'),parse_dates=[['YEAR', 'MONTH' ,'DAY','DAY_OF_WEEK']])
    return flights_data


class FlightsData(object):
    def __init__(self):
        self.flights_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'flights.csv'),parse_dates=[['YEAR', 'MONTH' ,'DAY','DAY_OF_WEEK']])

    def get(self, col_name):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Column {} doesn't exist".format(col_name))

    def create(self, data = None):
        col_name = data.keys()
        self.flights_data[col_name] = data.values()
        return self.flights_data

    def update(self, old_col, new_col):
        # original_col = self.get(old_col)
        self.flights_data[self.flights_data['AIRLINE'] == old_col] = new_col
        return self.flights_data

    def delete(self, col_name):
        self.flights_data.drop(col_name)

flight_data = FlightsData()


@ns_flight.route('/cols','/cols/<string:col_name>')
class TopColData(Resource):
    def get(self, col_name=None):
        if col_name:
            return_val = get_flights_data()[col_name].head(20)
            return_val = return_val.to_json(orient="records")
        else:
            return_val = jsonify(get_flights_data().columns.tolist())

        return json.dumps(return_val)

@ns_flight.route('/airlinedata','/airlinedata/<string:airline_name>')
class AirlineData(Resource):
    def get(self, airline_name=None):
        if airline_name:
            data = get_flights_data()
            return_val = (data[data['AIRLINE'] == airline_name].head(20))
            return_val = json.loads(return_val.to_json())
        else:
            return_val = jsonify(get_flights_data().AIRLINE.unique().tolist())

        return return_val


@ns_flight.route('/updateairline/<string:airline_code>', methods=['PUT'])
class ModifyAirlineCode(Resource):
    @ns_flight.doc('update_flights')
    # @ns_flight.marshal_list_with(flight_data)
    def put(self, airline_code):
        new_airline_code = request.form['new_airline_code']
        if airline_code is None:
            abort(400, custom='airline code is invalid')
        elif new_airline_code is None:
            abort(400, custom='airline code to be updated is invalid')
        else:
            data = get_flights_data()
            data[data['AIRLINE'] == airline_code ] = new_airline_code
            return_val = data[data['AIRLINE'] == airline_code ].head()

        return json.loads(return_val.to_json())


@ns_flight.route('/addairline', methods=['POST'])
class AddAirlineCode(Resource):
    @ns_flight.doc('add_flights')
    # @ns_flight.marshal_list_with(flight_data)
    def post(self):
        data = request.form['data']
        if data is None:
            abort(400, custom='data to be updated is invalid')
        else:
            data = get_flights_data()
            df2 = pd.DataFrame(data)
            data.append(df2)
            return_val = data[data['AIRLINE'] == data["AIRLINE"]].head()

        return json.loads(return_val.to_json())

if __name__ == '__main__':
    app.run(debug=True)