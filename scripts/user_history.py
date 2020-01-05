import json
from neo4j import GraphDatabase, basic_auth
from helpers import format_node, format_cypher_list
from random import randint
from datetime import date, timedelta


# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def enroll_user_in_course(user, course_id, enrollment, session):
    query = '''MATCH (c:Course), (u:User)
               WHERE c.course_id = $course_id AND u.id = $user_id
               CREATE (u)-[r:ENROLLED $enrollment]->(c)
               RETURN type(r)'''

    result = session.run(query, course_id=course_id,
                         user_id=user['id'], enrollment=enrollment)


def add_enrollment_info(courses, completed=True):
    num_of_course = len(courses)
    enrollment = {}
    current_date = date.today()
    course_start = timedelta(days=20)

    for course in courses:
        enrollment[course['course_id']] = {
            'enrollment_date': str(current_date - course_start),
            'completion_date': str(current_date) if completed else None,
            'status': 'COMPLETED' if completed else 'IN_PROGRESS'
        }

        current_date = current_date - course_start

    return enrollment


def seed_user_history(driver):
    # Load Data
    db = driver.session()
    # Load users
    users = format_cypher_list(db.run('MATCH (n:User) RETURN n'))
    # Load tags with more than one relationships
    tags = format_cypher_list(
        db.run('MATCH p=()-[r:RELATED_TO]->(n) WITH n, count(r) as rel_count WHERE rel_count > 2 RETURN DISTINCT n'))
    all_courses = format_cypher_list(db.run("MATCH (c:Course) RETURN c"))

    for user in users:
        # Choose a random tag
        random_tag = tags[randint(0, len(tags)) - 1]['knowledge']

        # Choose all the courses related to a tag
        courses = format_cypher_list(
            db.run("MATCH (c:Course)-[r:RELATED_TO]->(k:Knowledge) WHERE k.knowledge = $random_tag RETURN DISTINCT c",
                   random_tag=random_tag))

        enrollment = add_enrollment_info(courses)

        # Enroll users
        for course in courses:
            enroll_user_in_course(
                user, course['course_id'], enrollment[course['course_id']], db)

        # Give users a random course that is unfinished.
        random_course = [all_courses[randint(0, len(all_courses) - 1)]]

        if random_course not in courses:
            random_course_enrollment = add_enrollment_info(
                random_course, completed=False)

            enroll_user_in_course(user,
                                  random_course[0]['course_id'],
                                  random_course_enrollment[random_course[0]
                                                           ['course_id']],
                                  db)

    db.close()
