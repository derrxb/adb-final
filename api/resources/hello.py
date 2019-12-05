from api.models.author import Author
from flask_restful import Resource


class HelloWorld(Resource):
    """Example API"""

    def get(self):
        a = Author('david').add_author('This is a test')

        return {'hello': 'world'}
