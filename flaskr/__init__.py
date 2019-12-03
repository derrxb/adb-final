import os

from flask import Flask
from neo4j import GraphDatabase, basic_auth
from flask_restful import Resource, Api
from flask_cors import CORS

# Link the app to the Flask database
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j', 'password'))


# Factory to create the app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


# Create instance of the application
app = create_app()

# Wrap app with API to enable Flask-REST API
api = Api(app)


class HelloWorld(Resource):
    """Example API"""

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

# Enable debugging mode for dev environment
if __name__ == '__main__':
    app.run(debug=True)
