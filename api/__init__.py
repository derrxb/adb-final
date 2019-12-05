import os
from flask import Flask
from flask_cors import CORS
from neo4j import GraphDatabase, basic_auth


def create_app(test_config=None):
    # Factory to create the app
    # create and configure the app
    initApp = Flask(__name__, instance_relative_config=True)
    initApp.config.from_mapping(SECRET_KEY='dev')

    CORS(initApp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        initApp.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        initApp.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(initApp.instance_path)
    except OSError:
        pass

    return initApp


# Create instance of the application
app = create_app()
app.secret_key = os.urandom(24)

# Link the app to the Flask database
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))
