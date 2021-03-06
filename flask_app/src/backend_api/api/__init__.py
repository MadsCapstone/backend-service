"""API blueprint configuration."""
from flask import Blueprint
from flask_restx import Api
from backend_api.api.auth.endpoints import auth_ns
from backend_api.api.datatest.endpoints import datatest_ns
from backend_api.api.species.endpoints import species_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Capstone REST APIs",
    description="Welcome to the Swagger UI documentation site!",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(datatest_ns, path="/datatest")
api.add_namespace(species_ns, path="/species")