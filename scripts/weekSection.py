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


def add_weekSection(driver):
    """Add the languages to the database"""
    # Create session
    session = driver.session()

    # Get weekly data
    weekList = []
    for courseId, courseItem in data['WeekSection'].items():
        if courseItem is None:  # Courses that has no weekly information
            continue
        elif type(courseItem[0]) == str:  # Courses that only have week names
            for weekNum, weekItem in enumerate(courseItem, 1):
                weekData = {
                    'course_id': courseId,
                    'week_num': weekNum,
                    'week_name': weekItem,
                    'week_description': None,
                    'week_timeCommitment': None,
                    'week_id': None,
                    'week_slug': None
                }
        elif 'name' in courseItem[0].keys():  # Coursera courses
            for weekNum, weekItem in enumerate(courseItem, 1):
                weekData = {
                    'course_id': courseId,
                    'week_num': weekNum,
                    'week_name': weekItem['name'],
                    'week_description': weekItem['description'],
                    'week_timeCommitment': weekItem['timeCommitment'],
                    'week_id': weekItem['id'],
                    'week_slug': weekItem['slug']
                }
                weekList.append(weekData)
        elif 'sectionTitle' in courseItem[0].keys():  # eWant courses
            for weekNum, weekItem in enumerate(courseItem, 1):
                if type(weekItem['sectionDetail']) == str:
                    weekData = {
                        'course_id': courseId,
                        'week_num': weekNum,
                        'week_name': weekItem['sectionTitle'],
                        'week_description': weekItem['sectionDetail'],
                        'week_timeCommitment': None,
                        'week_id': None,
                        'week_slug': None
                    }
                    weekList.append(weekData)
                # eWant courses with descriptions in list form (multiple contents in a week)
                else:
                    weekData = {
                        'course_id': courseId,
                        'week_num': weekNum,
                        'week_name': weekItem['sectionTitle'],
                        'week_description': ' '.join(weekItem['sectionDetail']),
                        'week_timeCommitment': None,
                        'week_id': None,
                        'week_slug': None
                    }
                    weekList.append(weekData)

    # Load dictionary to neo4j
    for dicts in weekList:
        session.run('CREATE (w:weekSection) SET w = {dict_param}', parameters={
                    'dict_param': dicts})
    session.close()
    print('Weekly data addeed.')

    return weekList


if __name__ == '__main__':
    add_weekSection(driver)
