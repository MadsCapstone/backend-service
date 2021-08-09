"""Class definition for User model."""
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from backend_api import db, bcrypt
from backend_api.util.result import Result
from backend_api.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)

class Datatest(db.Model):
    "test data model for storing whatever and such"
    __tablename__ = "test_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date = db.Column(db.DateTime)
    data = db.Column(db.String(255))

    def __repr__(self):
        return (
            f"<id={self.id}, name= {self.name}, date={self.date}, data={self.data}>"
        )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_records(cls):
        return cls.query.all()

