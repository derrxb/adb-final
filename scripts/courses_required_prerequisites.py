import json
from neo4j import GraphDatabase, basic_auth
from helpers import contains, get_connection_details

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


# Relationships: Prerequisite; Required
A = ['I', 'A', '1']
B = ['II', 'B', '2']
C = ['III', 'C', '3']
D = ['IV', 'D', '4']
E = ['V', 'E', '5']
part_identifier = ['Course', 'Part', 'Health', 'Models', 'Data Science']


def by_identifier(identifier, count):
    return list(map(lambda x: f"{identifier} {x}", count))


def setup_prerequisite(course_a, course_b, session):
    """Set course_a as the prerequisite of course b"""
    query = '''MATCH (source:Course), (target:Course)
               WHERE source.course_id = $course_b AND target.course_id = $course_a
               CREATE (target)-[r:PREREQUISITE]->(source)
               RETURN type(r)'''

    session.run(
        query, course_a=course_a['course_id'], course_b=course_b['course_id'])


def setup_required(course_a, course_b, session):
    """Set course_a as the prerequisite of course b"""
    query = '''MATCH (source:Course), (target:Course)
               WHERE source.course_id = $course_b AND target.course_id = $course_a
               CREATE (target)-[r:REQUIRES]->(source)
               RETURN type(r)'''

    session.run(
        query, course_a=course_a['course_id'], course_b=course_b['course_id'])


def create_relationships(identifier, driver):
    """Creates Prerequisite and Required relationships between charges"""
    db = driver.session()

    like = f".*{identifier}.*"
    results = db.run(
        "MATCH (n:Course) WHERE n.title =~ $like RETURN n", like=like).values()

    courses = list(map(lambda x: dict(x[0].items()), results))

    part_1 = by_identifier(identifier, A)
    part_2 = by_identifier(identifier, B)
    part_3 = by_identifier(identifier, C)
    part_4 = by_identifier(identifier, D)
    part_5 = by_identifier(identifier, E)

    for course_a in courses:
        for course_b in courses:
            # Only if two courses have the almost the same title we set up this relationship.
            if course_a['title'] != course_b['title'] and course_a['title'].split(identifier)[0] in course_b['title']:
                # Assign the relationships
                if contains(course_a['title'], part_1) and contains(course_b['title'], part_2):
                    setup_prerequisite(course_a, course_b, db)
                    setup_required(course_b, course_a, db)
                elif contains(course_a['title'], part_2) and contains(course_b['title'], part_3):
                    setup_prerequisite(course_a, course_b, db)
                    setup_required(course_b, course_a, db)
                elif contains(course_a['title'], part_3) and contains(course_b['title'], part_4):
                    setup_prerequisite(course_a, course_b, db)
                    setup_required(course_b, course_a, db)
                elif contains(course_a['title'], part_4) and contains(course_b['title'], part_5):
                    setup_prerequisite(course_a, course_b, db)
                    setup_required(course_b, course_a, db)

    db.close()


def create_prerequisites_and_required(driver):
    """Creates Prerequisite and Required relationships between charges"""
    for divider in part_identifier:
        create_relationships(divider, driver)


if __name__ == '__main__':
    create_prerequisites_and_required(driver)
