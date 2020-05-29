# web_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Strains(db.Model):
    """
    Models the database entry for a Strain

    Model Members:
    -------------
        index = db.Column(db.BigInteger, primary_key=True)
        id = db.Column(db.BigInteger, nullable=False)
        name = db.Column(db.String(128), nullable=False)
        race = db.Column(db.String(128), nullable=False)
        flavors = db.Column(db.String(128), nullable=False)
        positive = db.Column(db.String(128))
        negative = db.Column(db.String(128))
        medical = db.Column(db.String(128))
        description = db.Column(db.String(128))
    """
    index = db.Column(db.BigInteger, primary_key=True)
    id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    race = db.Column(db.String(128), nullable=False)
    flavors = db.Column(db.String(128), nullable=False)
    positive = db.Column(db.String(128), nullable=False)
    negative = db.Column(db.String(128), nullable=False)
    medical = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128), nullable=False)


def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a
    list of dictionaries, so they can be returned as JSON

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    try:
        for record in database_records:
            parsed_record = record.__dict__
            del parsed_record["_sa_instance_state"]
            parsed_records.append(parsed_record)
    except:
        parsed_record = database_records.__dict__
        del parsed_record["_sa_instance_state"]
        return parsed_record
