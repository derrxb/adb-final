import json
from neo4j import GraphDatabase, basic_auth
from scripts.courses import add_course
from scripts.languages import add_languages

file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


def get_by_key(key): return data[key]


# Breaks down the items by the top level directory
authors = get_by_key(data, 'Author')
descriptions = get_by_key(data, 'Description')
direct_links = get_by_key(data, 'DirectLink')
languages = get_by_key(data, 'Language')
photo_links = get_by_key(data, 'PhotoLink')
providers = get_by_key(data, 'Provider')
titles = get_by_key(data, 'Title')
week_sections = get_by_key(data, 'WeekSection')
knowledges = get_by_key(data, 'Knowledge')


driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def seed_data(driver):
    # Set up database connection
    session = driver.session()

    # We start with the courses basic information
    for _, course in enumerate(titles.items()):
        course_id = course[0]

        # Add records and create links until all the information is added
        course = add_course(driver, course_id)
        language = add_languages(driver)

        # Link course to language
