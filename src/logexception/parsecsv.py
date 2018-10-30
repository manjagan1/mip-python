from src.logexception.exceptionhandler import exception_handler
# Error & Exception handling
import logging
from src.logexception.logframework import LoggerInitialiser
# import src.logexception.module_logger as ml

logger = logging.getLogger(__name__)
LoggerInitialiser(conf_method='yaml', conf_path='./config/log_config.yaml')

class ErrorInput(enumerate):
    ZERODIV = 1
    STRTYPE = 2
    OTHER = 3


@exception_handler
def parse_csv_and_get_columns(filename, error_req=None):
    csvFile = None
    try:
        csvFile = open(filename, 'r')
        lines = csvFile.readlines()
        for line in lines[1:]:
            val = line.split(",")
            if error_req == ErrorInput.STRTYPE:
                test_str_div = val[0] / val[11]
            elif error_req == ErrorInput.ZERODIV:
                test_zero_div =  (int(val[0]) / int(val[11]))
    #         elif error_req == ErrorInput.OTHER:
    #             raise UnAcceptedLenError(val)
    # except UnAcceptedLenError as e:
    #     logging.error ("unaccepted error ".format(e))
    # except (FileNotFoundError, TypeError, ZeroDivisionError) as e:
    #     logging.error (ApplicationException("hi guys!!! watch out ", e))
    # except Exception as e:
    #     logging.critical(ApplicationException("You should never come here!!! ", e))
    # finally:
    #     if csvFile:
    #         csvFile.close()
    #     pass


if __name__ == "__main__":
    logger.info("Input: non existant file and check for exceptions")
    parse_csv_and_get_columns(filename = "data/test.csv")

    logger.info("Divide strings to get the exeption")
    parse_csv_and_get_columns(filename = "../../data/flights.csv", error_req=ErrorInput.STRTYPE)

    logger.info("Divide by zero exception")
    parse_csv_and_get_columns(filename="../../data/flights.csv", error_req=ErrorInput.ZERODIV)

    logger.info("Custom Exception to be thrown")
    parse_csv_and_get_columns(filename="../../data/flights.csv", error_req=ErrorInput.OTHER)