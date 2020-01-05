
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
