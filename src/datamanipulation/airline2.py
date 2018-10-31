import pandas as pd
import numpy as np
import logging
from src.logexception.logframework import LoggerInitialiser, logging
import scipy

logger = logging.getLogger(__name__)

# read the csv file into a pandas dataframe
flights_df = pd.read_csv("../../data/flights.csv")

def calculate_metrics(data, metric_type, cols_input):
    # metric = data[cols_input].apply(np.mean)
    metric = data.groupby(cols_input).describe()
    kurt = data.groupby(cols_input).kurtosis()
    return metric

def remove_outliers(data, cols = "DEPARTURE_DELAY", normal = 3, ):
    # calculate the outliers outside of 3 standard deviation from mean
    mean = np.mean(data['DEPARTURE_DELAY'], axis=0)
    stddev = np.std(data['DEPARTURE_DELAY'], axis=0)

    def check(x):
        if (x > mean + 2 * stddev):
            return False
        else:
            return True

    final_list = data[cols].apply(lambda x:np.abs(x-x.mean())/ x.std() > normal )
    # final_list = [x for x in data['DEPARTURE_DELAY'] if ((x > mean - 2 * stddev) or (x < mean + 2 * stddev))]
    return final_list


def log_transform(data, cols = None):
    if cols is None:
        cols = list_all_quantitative_cols()

    def check(x):
        if x < 0:
            return 0.001
        else:
            return  x

    data_log = data[cols].applymap(lambda x:np.log(check(x)))
    return data_log


def percentage_delay_for_all_departure_airports(data):
    # For each airline, the percentage delay
    # for each dep_airport, over total delay across all dep_airport
    sum_of_departures = data[["AIRLINE","ORIGIN_AIRPORT","DEPARTURE_DELAY"]].groupby(["AIRLINE","ORIGIN_AIRPORT"]).agg('sum')
    total_delay_dep_airport = data["DEPARTURE_DELAY"].sum()
    return (data.apply(lambda x: 100 *x / data["DEPARTURE_DELAY"].sum()))

def average_delay(data):
    # Calculate the mean "Departure_delay" for each airline, over the whole dataset
    avg_delay_airline = data[["AIRLINE","DEPARTURE_DELAY"]].groupby("AIRLINE").mean()
    print (avg_delay_airline)

def less_than_12(data, percentage=False):
    data['before_12'] = data["SCHEDULED_DEPARTURE"].apply(lambda x: x < 1200)
    morning_flight = data[['before_12','AIRLINE']].groupby("AIRLINE").count()
    print (morning_flight)
    if percentage:
        morning_flight = morning_flight.apply(lambda x: 100 * x / float(x.sum()))
    return morning_flight

def create_route_cols():
    flights_df["Routes"] = flights_df[['ORIGIN_AIRPORT','DESTINATION_AIRPORT']].apply(lambda x: '->'.join(x), axis=1)
    print (flights_df["Routes"].head(5))

def list_all_quantitative_cols(data = None, filter_type = None):
    if data is None:
        return None
    if filter_type is None:
        filter_type = np.number

    columns_numeric = data.select_dtypes(include=[filter_type])
    return columns_numeric.columns.tolist()

def find_all_metrics(data = None, cols_needed = None):
    print ("find all means")
    if data is not None:
        desc_output = calculate_metrics(data=data, metric_type = "mean", cols_input=cols_needed)
    print (desc_output.head(5))
#     agg and q_25


def count_flights_per_route(data, percentage = False):
    # For each airline, the count of flights
    # for each Route(see task1), each route being a separate column
    data["Routes"] = data[['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']].apply(lambda x: '->'.join(x), axis=1)
    # data["AIRLINE", "Routes"]].groupby(by=("AIRLINE", "Routes"))["AIRLINE"].count()
    flight_count = pd.pivot_table(data[["AIRLINE", "Routes"]], index="AIRLINE", columns="Routes", aggfunc=len, fill_value=0)
    route_delay = pd.pivot_table(data[["AIRLINE", "Routes","DEPARTURE_DELAY"]], index="AIRLINE", columns="Routes", aggfunc=np.sum, fill_value=0, calc_percent=True)

    if percentage:
        data[["AIRLINE", "DEPARTURE_DELAY"]].groupby(by=("AIRLINE")).count()
        counts = flight_count.apply(lambda x: x.isnull().value_counts())

    return counts



if __name__ == "__main__":
    # create_route_cols()
    # find_all_metrics(flights_df,list_all_quantitative_cols(flights_df))
    # remove_outliers(flights_df)
    # average_delay(flights_df)
    # less_than_12(flights_df, percentage=True)
    # percentage_delay_for_all_departure_airports(flights_df)
    count_flights_per_route(flights_df, percentage=True)

