from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy import asc, text
from backend_api.models.waterbody import Waterbody, WaterBodyGeoJsonSchema, WaterBodySchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from marshmallow import Schema


from backend_api import db, bcrypt, ma
from backend_api.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)

class Species(db.Model):
    """Species name and id table"""
    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))

    @classmethod
    def get_name_by_species_id(cls, id):
        return cls.query.filter_by(id=id).first()

class InvasiveSpecies(db.Model):
    """Invasive Species id and name"""
    __tablename__ = "invasive_species"

    # uid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id = db.Column(db.Integer, primary_key=True) #TODO: Change to foreign key of species table when ready...
    name = db.Column(db.String(255))

    @classmethod
    def get_all(cls):
        return cls.query.order_by(text("name asc")).all()

class SpeciesObservedWaterbody(db.Model):
    """Describes a relationship between invasive species sighting
        and waterbodies they are found in
    """
    __tablename__ = "species_observed"
    uid = db.Column(db.Integer, primary_key=True, unique=True)
    species_id = db.Column(db.Integer, ForeignKey(Species.id))
    waterbody_id = db.Column(db.Integer, ForeignKey(Waterbody.id))
    waterbody_name = db.Column(db.String(255))
    distance = db.Column(db.Integer)

    @classmethod
    def find_invasive_waterways_by_species_id(cls, id):
        return cls.query.filter_by(species_id=id).all()


class ImpactRelationship(db.Model):
    """Impacter and Impactee Relationship"""
    __tablename__ = "impact_rel"

    impacter_id = db.Column(db.Integer, primary_key=True)
    impacted_id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def find_species_impact_by_id(cls, id):
        return cls.query.filter_by(impacter_id=id).all()

class ImpactRelationshipDistance(db.Model):
    """Relationship between species to make the vizualization for hierarchy"""
    __tablename__ = "impact_rel_dist"

    uid = db.Column(db.Integer, primary_key=True)
    impacter_id = db.Column(db.Integer, ForeignKey(Species.id))
    impacted_id = db.Column(db.Integer, ForeignKey(Species.id))
    distance = db.Column(db.Integer)

    @classmethod
    def find_invasive_impact_by_id(cls, id):
        return cls.query.filter_by(impacter=id).all()


"""Model section for schema marshalling"""
class InvasiveSpeciesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InvasiveSpecies
        include_relationships = True
        load_instance = True

class ImpactRelationshipDistanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ImpactRelationshipDistance
        include_relationships = True
        load_instance = True

class SpeciesObservedWaterbodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SpeciesObservedWaterbody
        include_relationships = True
        load_instance = True

class SpeciesObservedGeoJsonSchema(Schema):
    species_observed = fields.Nested(SpeciesObservedWaterbodySchema)
    waterbody_geojsons = fields.Nested(WaterBodyGeoJsonSchema)

class SpeciesObservedWaterBodyNested(Schema):
    species_observed = fields.Nested(SpeciesObservedWaterbodySchema)
    waterbody = fields.Nested(WaterBodySchema)

species_tables = {
    'species': Species,
    'invasive_species': InvasiveSpecies,
    'species_observed': SpeciesObservedWaterbody,
    'impact_rel': ImpactRelationship,
    'impact_rel_dist': ImpactRelationshipDistance
}