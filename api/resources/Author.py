# from api.models.author import Author
from flask_restful import Resource, abort
from api.models.author import Author


class AuthorResource(Resource):
    """Endpoint for Author"""

    def get(self, id):
        author = Author().find_by_id(id)

        if author == None:
            abort(404, error='Author not found')

        return author
