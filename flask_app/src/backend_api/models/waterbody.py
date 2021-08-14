"""Class definition for Waterbody models"""

from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from backend_api import db, bcrypt
from backend_api.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)

class Waterbody(db.Model):
    """Stores the information for the Waterbodies"""
    __tablename__ = "waterbody"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255)) #TODO: Fill out foreign key


class WaterBodyEdges(db.Model):
    """Stores the information for connected waterbodies"""
    __tablename__ = "waterbody_edges"
    nodei_id = db.Column(db.Integer, primary_key=True)
    nodef_id = db.Column(db.Integer, primary_key=True)

class WaterBodyMetaData(db.Model):
    """Defines metadata for a waterbody by id"""
    __tablename__ = "waterbody_metadata"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))

class WaterBodyGeoJson(db.Model):
    """Defines the waterbody geojson relationship for the frontend"""
    __tablename__ = "waterbody_geojson"

    uid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, ForeignKey(Waterbody.id), ForeignKey("species_observed.waterbody_id"))
    geojson = db.Column(db.JSON)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_ids(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).all()


"""Model section for schema marshalling"""
class WaterBodyGeoJsonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WaterBodyGeoJson
        include_relationships = True
        load_instance = True

class WaterBodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Waterbody
        include_relationships = True
        load_instance = True

waterbody_tables = {
    "waterbody": Waterbody,
    "waterbody_edges": WaterBodyEdges,
    "waterbody_metadata": WaterBodyMetaData,
    "waterbody_geojson": WaterBodyGeoJson,
}