# from backend_api.models.species import InvasiveSpecies, Species

from flask_restx import Model
from flask_restx.fields import String, Boolean
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser



species_reqparser = RequestParser(bundle_errors=True)
species_reqparser.add_argument(
    name="species_id", type=int, location="json", required=True, nullable=False
)

targetrel_reqparser = RequestParser(bundle_errors=True)
targetrel_reqparser.add_argument(
    name="name", type=str, location="json", required=True, nullable=False
)
targetrel_reqparser.add_argument(
    name="query_type", type=str, location="json", required=True, nullable=False
)

species_model = Model(
    "Species",
    {
        'species_id':String
    },
)

