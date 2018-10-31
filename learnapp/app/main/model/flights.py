from .. import db

class Flights(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)

    # def __repr__(self):
    #     return "<User '{}'>".format(self.username)