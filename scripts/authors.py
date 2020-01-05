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


def add_author(driver):
    session = driver.session()

    # use a set to avoid duplicates
    allauthors = set()

    for authors in data['Author'].values():
        if type(authors)is list:
            if authors:  # if list is not empty
                for person in authors:
                    if person != "":
                        allauthors.add(person)
        else:
            if authors != "":
                allauthors.add(authors)

    # print authors
    # for x in allauthors:
    #    print(x)

    allauthors = list(allauthors)

    # Load to neo4j
    for names in allauthors:
        session.run(
            'CREATE (a:Author {author: $author }) RETURN a', author=names)

    session.close()

    return len(allauthors)


if __name__ == '__main__':
    print("Authors added", add_author(driver))
