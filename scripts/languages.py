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


def add_language(driver):
    """Add the languages to the database"""
    # Create session
    session = driver.session()

    # Get unique languages
    languages = list(set(data['Language'].values()))

    # Create language nodes
    for language in languages:
        session.run(
            'CREATE (l:Language {language: $language }) RETURN l', language=language)

    session.close()
    print('Languages added')

    return languages


if __name__ == '__main__':
    print('Current languages: ', add_language(driver))
