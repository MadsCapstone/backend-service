"""API endpoint definitions for /datatests namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource
from flask import jsonify

from backend_api.api.datatest.dto import datatest_model, datatest_model_ma


datatest_ns = Namespace(name="datatest", validate=True)
datatest_ns.models[datatest_model.name] = datatest_model

@datatest_ns.route("/alldata", endpoint="all_data")
class AllData(Resource):
    """Gets all test data from database for testing connections"""

    @datatest_ns.response(int(HTTPStatus.OK), "Retrieved all users")
    @datatest_ns.response(int(HTTPStatus.BAD_REQUEST), "Request Was Bad")
    @datatest_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get all test data"""
        return jsonify(
            data="all the data you will ever want"
        )


