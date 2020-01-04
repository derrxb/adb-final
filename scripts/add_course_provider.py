import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def add_course_provider(driver):
    session = driver.session()
    for _, course in enumerate(data['Title'].items()):
        course_id = course[0]
        course_provider = data['Provider'][course_id]
        result = session.run(
            'MATCH (c:Course), (p:Provider) WHERE c.course_id = $course_id AND p.provider = $course_provider CREATE (c)-[r:PROVIDED_BY]->(p) RETURN type(r)', course_id=course_id, course_provider=course_provider)
    print(course_provider)

add_course_provider(driver)
