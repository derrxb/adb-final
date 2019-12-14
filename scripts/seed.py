import json
from neo4j import GraphDatabase, basic_auth
from courses import add_course
from languages import add_language
from provider import add_provider
from knowledge import add_knowledge
from weekSection import add_weekSection
from authors import add_author

file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def seed_data(driver):
    # Set up database connection
    session = driver.session()

    # We start with the courses basic information
    for _, course in enumerate(data['Title'].items()):
        course = add_course(driver, course[0])

    language = add_language(driver)
    providers = add_provider(driver)
    tags = add_knowledge(driver)
    week = add_weekSection(driver)
    authors = add_author(driver)


seed_data(driver)
