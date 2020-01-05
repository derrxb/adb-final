import json
from neo4j import GraphDatabase, basic_auth
from helpers import format_node, format_cypher_list
from random import randint


# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def enroll_user_in_course(user, course_id, session):
    query = '''MATCH (c:Course), (u:User)
               WHERE c.course_id = $course_id AND u.id = $user_id
               CREATE (u)-[r:ENROLLED]->(c)
               RETURN type(r)'''

    result = session.run(query, course_id=course_id, user_id=user['id'])


def seed_user_history(driver):
    # Load Data
    db = driver.session()
    # Load users
    users = format_cypher_list(db.run('MATCH (n:User) RETURN n'))
    # Load tags with more than one relationships
    tags = format_cypher_list(
        db.run('MATCH p=()-[r:RELATED_TO]->(n) WITH n, count(r) as rel_count WHERE rel_count > 2 RETURN DISTINCT n'))

    for user in users:
        # Choose a random tag
        random_tag = tags[randint(0, len(tags)) - 1]['knowledge']

        # Choose all the courses related to a tag
        courses = format_cypher_list(
            db.run("MATCH (c:Course)-[r:RELATED_TO]->(k:Knowledge) WHERE k.knowledge = $random_tag RETURN DISTINCT c",
                   random_tag=random_tag))

        # Enroll users
        for course in courses:
            enroll_user_in_course(user, course['course_id'], db)

    db.close()
