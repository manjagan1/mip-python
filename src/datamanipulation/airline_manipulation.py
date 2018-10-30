import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def transform_data():
    # read the csv file into a pandas dataframe
    flights_df = pd.read_csv("../../data/flights.csv")

    # list all the column headers
    logger.info ("List the orignal column header",list(flights_df))

    # remove the columns Days_of_week from the dataframe
    flights_df.drop("DAY_OF_WEEK", inplace=True, axis = 1)

    # rename the columns wheels_off to has_wheels
    flights_df.rename(index = str,columns = {"WHEELS_OFF":"HAS_WHEELS"}, inplace=True)

    # list the flights df with the renamed header
    logger.info ("List the renamed column headers",list(flights_df))

    # split the pandas dataframe into 4 equal parts row wise
    splits = np.array_split(flights_df, 4)
    logger.info ("split0",splits[0].head(5))
    logger.info ("split1",splits[1].head(5))

    # concatenate the chunks into 1 dataset
    full_df = pd.concat(splits)
    logger.info ("combined",full_df.head(5))

    # get the slice of the dataset that is only relevant to the airline AA
    airline_aa = flights_df.loc[flights_df['AIRLINE'] == 'AA']

    # get the slice of the data where delay < 10 and destination in pbi
    custom_delay = flights_df.loc[(flights_df['DEPARTURE_DELAY'] < 10) & (flights_df['DESTINATION_AIRPORT'] == "PBI")]
    logger.info(custom_delay.head(5))

    # fill the blanks in the AIR_SYSTEM_DELAY column with the average of the column itself
    flights_df['AIR_SYSTEM_DELAY'].fillna((flights_df['AIR_SYSTEM_DELAY'].mean()), inplace=True)
    logger.info (flights_df['AIR_SYSTEM_DELAY'].head(5))

    # Airline which contains A, keep it in a separate column
    flights_df['has_A'] = flights_df['AIRLINE'].str.contains('A')
    logger.info(flights_df)

    # get a random sample of the rows in the dataframe
    logger.info (flights_df.sample(10))


    # normalise the column "DEPARTURE_DELAY" to the range 0 - 1 with MinMax normalisation
    normalized_df = (flights_df["DEPARTURE_DELAY"] - flights_df["DEPARTURE_DELAY"].min()) / (flights_df["DEPARTURE_DELAY"].max() - flights_df["DEPARTURE_DELAY"].min())
    logger.info ("normalized df", normalized_df)

    # binarize the column ORIGIN_AIRPORT
    binarize = pd.get_dummies(flights_df['ORIGIN_AIRPORT'])
    logger.info (binarize.head(5))

    return flights_df

if __name__ == "__main__":
    transform_data()

    # workflow engine orchestration capability to schedule a->b-c..configure the branching write the exit log.
    # base job -> inheriting job -> writeback -> readback
