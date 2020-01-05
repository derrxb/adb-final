import json
from neo4j import GraphDatabase, basic_auth
from helpers import format_node
from random import randint


# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def enroll_user_in_course(user, course_id, driver):
    db = driver.session()

    query = '''MATCH (c:Course), (u:User)
               WHERE c.course_id = $course_id AND u.id = $user_id
               CREATE (u)-[r:ENROLLED]->(course)
               RETURN type(r)'''

    result = db.run(query, course_id=course_id, user_id=user['id'])

    db.close()


def seed_user_history(driver):
    # Load Data
    db = driver.session()
    results = db.run('MATCH (n:User) RETURN n')
    users = list(map(lambda x: format_node(x.value()), results))
    db.close()

    for user in users:
        for _ in range(5):
            course_id = str(randint(1, 825))
            course_title = data['Title'][str(course_id)]

            enroll_user_in_course(user, course_id, driver)

    db.close()


seed_user_history(driver)
