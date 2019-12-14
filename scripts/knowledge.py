import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('../data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=('neo4j',  'password'))


def add_knowledge(driver):
    session = driver.session()

    # get unique knowledge tags
    knowledge =  data['Knowledge'].values()

    tags = set()

    for lists in knowledge:
        for word in lists:
            tags.add(word)

    tags = list(tags)
    print(tags)
    print(len(tags))

    # add tags
    for tag in tags:
        session.run(
            'CREATE (k:knowledge {knowledge: $knowledge }) RETURN k', knowledge=tag)

    session.close()

    return tags

print("Knowledge added:", add_knowledge(driver))
