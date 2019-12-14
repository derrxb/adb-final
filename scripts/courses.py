import json
from neo4j import GraphDatabase, basic_auth

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
    result = session.run('CREATE (c:Course $course) RETURN c', course=course)

    return result.single()
