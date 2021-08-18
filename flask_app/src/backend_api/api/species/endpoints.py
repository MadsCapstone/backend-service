"""API endpoint definitions for /species namespace"""

from http import HTTPStatus

from flask_restx import Namespace, Resource
from flask import jsonify

from backend_api.models.species import Species, InvasiveSpecies
from backend_api.api.species.business import *
from backend_api.api.species.dto import species_reqparser, species_model, targetrel_reqparser


species_ns = Namespace(name='species', validate=True)
species_ns.models[species_model.name] = species_model #TODO: Add models

@species_ns.route("/invasive", endpoint='Invasive Species')
class InvasiveSpecies(Resource):
    """Get all the invasive species as json for the front end"""

    @species_ns.response(int(HTTPStatus.OK), "Retrieved all Invasive Species")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get invasive species data from the Invasive Species database"""
        invasives = get_invasive_species()
        return invasives


@species_ns.route("/observed", endpoint="Species Observations")
class ObservedSpecies(Resource):
    """Get information on the observed species id and where they were observed"""

    @species_ns.expect(species_reqparser)
    @species_ns.response(int(HTTPStatus.OK), "Retrieved all Invasive Species")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Get observations and waterways by species_id"""
        request_data = species_reqparser.parse_args()
        species_id = request_data.get('species_id')
        data = get_species_observations(species_id)
        return data

@species_ns.route("/impact", endpoint="Impact Relationships by Species_id")
class ImpactRelationship(Resource):
    """Get the json needed to build network of impact by species id"""
    @species_ns.expect(species_reqparser)
    @species_ns.response(int(HTTPStatus.OK), "Retrieved impact network for requested species")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Get the impact relationships with focus node of species_id"""
        request_data = species_reqparser.parse_args()
        species_id = request_data.get('species_id')
        payload = get_impact_network(species_id)
        print(payload)
        return payload

@species_ns.route("/impactnetwork", endpoint="Impact Network For All")
class ImpactWeb(Resource):
    """Get the json needed to build network of impact by species id"""
    @species_ns.response(int(HTTPStatus.OK), "Retrieved impact network successfully")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get the impact relationships of all nodes (impact web)"""
        pass

@species_ns.route("/targetinvasive", endpoint="Invasives for target vizualization")
class InvasiveSpeciesTargetDropdown(Resource):
    """Defines endpoint for getting target invasives"""

    @species_ns.response(int(HTTPStatus.OK), "Retrieved impacters list successfully")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get the impacter dropdown set of species"""
        payload = get_target_invasive_dropdown()
        return payload

@species_ns.route("/targetimpacted", endpoint="Impacted species for target vizualization")
class ImpactedSpeciesTargetDropdown(Resource):
    """Defines endpoint for getting target impacted"""

    @species_ns.response(int(HTTPStatus.OK), "Retrieved impacted species successfully")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get the impacter dropdown set of species"""
        payload = get_target_impacted_dropdown()
        return payload

@species_ns.route("/targetimpactrel", endpoint="Get data for target visualization")
class TargetImpactRelationship(Resource):
    """Defines endpoint for getting target viz relationship data"""

    @species_ns.expect(targetrel_reqparser)
    @species_ns.response(int(HTTPStatus.OK), "Retrieved impact target viz successfully")
    @species_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @species_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Get the impacter dropdown set of species"""
        requestdata = targetrel_reqparser.parse_args()
        query_type = requestdata.get('query_type')
        name = requestdata.get('name')
        payload = get_target_relationship_data(name, query_type)
        return payload

