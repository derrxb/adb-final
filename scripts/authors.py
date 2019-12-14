import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('../data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=('neo4j',  'password'))


def add_author(driver):
    session = driver.session()

    # get unique author tags
    author =  data['Author'].values()

    tags = set()

    for lists in author:
        for word in lists:
            if word != "":
                tags.add(word)

    tags = list(tags)
    print(tags)
    print(len(tags))

    # add tags
    for tag in tags:
        session.run(
            'CREATE (a:author {author: $author }) RETURN a', author=tag)

    session.close()

    return tags

print("Author added:", add_author(driver))
