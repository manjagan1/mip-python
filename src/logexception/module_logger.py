import logging

module_logger = logging.getLogger(__name__)
print(__name__)

def alive_again():
    module_logger.error('I CAN SEE YOU FROM MODULE!!!!!!!!!')