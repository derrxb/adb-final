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


def add_course_keywords(driver):
    session = driver.session()
    for _, course in enumerate(data['Title'].items()):
        course_id = course[0]
        course_knowledge_list = data['Knowledge'][course_id]

        for course_knowledge in course_knowledge_list:
            # print(course_knowledge)
            result = session.run(
                'MATCH (c:Course), (k:Knowledge) WHERE c.course_id = $course_id AND k.knowledge = $course_knowledge CREATE (c)-[r:RELATED_TO]->(k) RETURN type(r)', course_id=course_id, course_knowledge=course_knowledge)

    session.close()
    return "Keyword-Course Relationships created."


if __name__ == '__main__':
    print(add_course_keywords(driver))
