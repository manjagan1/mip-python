
from src.flaskapp.app import api

class FlaskAPPException(Exception):
    pass


@api.error_handlers()

