import json
from neo4j import GraphDatabase, basic_auth
from helpers import contains

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def add_course(driver, course_id):
    """Adds a course using its `course_id`."""

    # Create Session
    session = driver.session()

    # Course information
    course = {
        'course_id': course_id,
        'title': data['Title'][course_id],
        'description': data['Description'][course_id] or 'No Description',
        'direct_link': data['DirectLink'][course_id] or 'No direct link',
        'photo_link': data['PhotoLink'][course_id] or 'No photo link',
    }

    # Add the course to the database
    result = session.run(
        'CREATE (c:Course $course) RETURN c', course=course).single()[0]

    session.close()

    add_course_level(result, driver)

    return result


def create_course_levels(driver):
    """Creates course difficulties levels"""
    session = driver.session()

    levels = ['neutral', 'basic', 'intermediate', 'advanced']

    for level in levels:
        session.run("CREATE (l:Level {name: $name })", name=level)

    session.close()


def add_course_level(result, driver):
    """Links a course to a certain `difficulty` level"""
    session = driver.session()
    course = dict(result.items())
    level = 'neutral'

    title = course['title'].lower()

    if contains(title, ['basic', 'essential', 'fundamental', 'introduction']):
        level = 'basic'

    if contains(title, ['intermediate']):
        level = 'intermediate'

    if contains(title, ['advanced']):
        level = 'advanced'

    if course['description'] is not None and level == 'neutral':
        description = course['description'].lower()

        if contains(description, ['basic', 'essential', 'fundamental', 'introduction']):
            if not contains(description, ['advanced']):
                level = 'basic'
            elif contains(description, ['intermediate']):
                level = 'intermediate'
            elif contains(description, ['advanced']):
                level = 'advanced'

    query = '''MATCH (source:Level), (target:Course)
               WHERE source.name = $level AND target.course_id = $course_id
               CREATE (target)-[r:DIFFICULTY]->(source)
               RETURN type(r)'''

    session.run(query, level=level, course_id=course['course_id'])

    session.close()
