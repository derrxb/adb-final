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


def add_course_weeks_section(driver):
    session = driver.session()

    for _, course in enumerate(data['Title'].items()):
        course_id = course[0]
        week_sections = data['WeekSection'][course_id]

        if week_sections == None:
            continue
        else:
            # Since in the WeekSection seed file the course_id is added to
            # to the week data, we can simply link the week sections and course
            # through the course id. The downside of this is that in this case,
            # we're using the week sections in a relational kind of way.
            query = '''MATCH (c:Course), (w:weekSection)
                       WHERE c.course_id = $course_id AND w.course_id = $course_id
                       CREATE (c)-[r:DIVIDED_INTO]->(w)
                       RETURN type(r)'''

            session.run(query, course_id=course_id)

    session.close()

    print('Linked Course and Week Section Data')


if __name__ == '__main__':
    add_course_weeks_section(driver)
