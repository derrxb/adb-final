# from api.models.author import Author
from flask_restful import Resource, abort
from api.models.author import Author
from api.common.cypher_helpers import page_number, page_size


class AuthorsResource(Resource):
    """Endpoint for all Authors"""

    def get(self):
        authors = Author().find_all(page_number(), page_size())

        if authors == None:
            abort(404, error='Authors not found')

        return authors
