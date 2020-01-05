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


def add_course_lang(driver):
    session = driver.session()
    for _, course in enumerate(data['Title'].items()):
        # print(course)
        course_id = course[0]
        course_language = data['Language'][course_id]
        result = session.run(
            'MATCH (c:Course), (l:Language) WHERE c.course_id = $course_id AND l.language = $course_language CREATE (c)-[r:CONDUCTED_IN]->(l) RETURN type(r)', course_id=course_id, course_language=course_language)


if __name__ == '__main__':
    add_course_lang(driver)
