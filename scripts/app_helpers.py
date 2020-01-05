from flask import g
from api import driver, app


def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    else:
        g.neo4j_db.close()
        g.neo4j_db = driver.session()

    return g.neo4j_db


@app.teardown_appcontext
def close_db(error=None):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()
