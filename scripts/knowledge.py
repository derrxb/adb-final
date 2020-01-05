import json
from neo4j import GraphDatabase, basic_auth
from helpers import get_connection_details

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

graphenedb_url = get_connection_details()[0]
graphenedb_user = get_connection_details()[1]
graphenedb_pass = get_connection_details()[2]

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver(graphenedb_url,
                              auth=basic_auth(graphenedb_user, graphenedb_pass))


def add_knowledge(driver):
    session = driver.session()

    # get unique knowledge tags
    knowledge = data['Knowledge'].values()

    tags = set()

    for lists in knowledge:
        for word in lists:
            tags.add(word)

    tags = list(tags)
    # print(tags)
    # print(len(tags))

    # add tags
    for tag in tags:
        session.run(
            'CREATE (k:Knowledge {knowledge: $knowledge }) RETURN k', knowledge=tag)

    session.close()

    return len(tags)


if __name__ == '__main__':
    print("Knowledge added:", add_knowledge(driver))
