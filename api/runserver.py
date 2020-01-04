import os
from flask import Flask, g, Blueprint
from flask_restful import Api
from flask_cors import CORS
from .resources.Author import AuthorResource
from .resources.Authors import AuthorsResource
from .resources.Courses import CoursesResource
from api import app

# Wrap app with API to enable Flask-REST API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(AuthorsResource, '/authors')
api.add_resource(AuthorResource, '/authors/<int:id>')
api.add_resource(CoursesResource, '/courses')
app.register_blueprint(api_bp)

print(app.url_map)

# Enable debugging mode for dev environments
if __name__ == '__main__':
    app.run(debug=True)
