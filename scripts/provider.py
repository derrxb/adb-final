import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def add_provider(driver):
    """Add the Provider information to the database"""
    # Create session
    session = driver.session()

    # Get unique providers
    providers = list(set(data['Provider'].values()))

    # Create provider nodes
    for provider in providers:
        session.run(
            'CREATE (p:Provider {provider: $provider }) RETURN p', provider=provider)

    session.close()

    return providers


# print('Current providers: ', add_provider(driver))
