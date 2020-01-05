import os


def get_connection_details():
    # Publish in heroku
    graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")

    # for running in local computer
    if not graphenedb_url or graphenedb_url == '':
        graphenedb_url = 'bolt://localhost:7687'
    if not graphenedb_user or graphenedb_user == '':
        graphenedb_user = 'neo4j'
    if not graphenedb_pass or graphenedb_pass == '':
        graphenedb_pass = 'password'

    return [graphenedb_url, graphenedb_user, graphenedb_pass]


def clear_db(driver):
    """Removes all the records from the database to give you a clean slate"""
    session = driver.session()

    session.run("MATCH(n) OPTIONAL MATCH(n)-[r]-() DELETE n, r")

    session.close()

    print("Successfully removed Data and Relationships from database")


def contains(text, array=[]):
    """Determines if any of the provided strings in an array is included in a text"""
    contains = False

    for word in array:
        if word in text:
            contains = True
            break

    return contains


def format_node(node):
    """Formats a Neo4j Node to JSON Object"""
    temp = dict(node.items())
    temp['node_id'] = node.id
    temp['node_type'] = list(node.labels)[0]

    return temp


def format_cypher_list(query_results):
    """Converts a Cypher query results into a JSON object"""
    return list(map(lambda x: format_node(x.value()), query_results))
