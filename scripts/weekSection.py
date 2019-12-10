import json
from neo4j import GraphDatabase, basic_auth
from pprint import pprint

file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def add_weekSection(driver):
    """Add the languages to the database"""
    # Create session
    session = driver.session()

    # Get
    weekList = []
    for courseId, courseItem in data['WeekSection'].items():
        if courseItem is None:
            weekData = {
              'course_id':courseId,
              'week_num':None,
              'week_name':None,
              'week_description':None,
              'week_timeCommitment':None,
              'week_id':None,
              'week_slug':None
              }
            weekList.append(weekData)
        elif type(courseItem[0]) == str:
            for weekNum, weekItem in enumerate(courseItem,1):
                weekData = {
                    'course_id':courseId,
                    'week_num':weekNum,
                    'week_name':weekItem,
                    'week_description':None,
                    'week_timeCommitment':None,
                    'week_id':None,
                    'week_slug':None
                    }
        elif 'name' in courseItem[0].keys():
            for weekNum, weekItem in enumerate(courseItem,1):
                weekData = {
                    'course_id':courseId,
                    'week_num':weekNum,
                    'week_name':weekItem['name'],
                    'week_description':weekItem['description'],
                    'week_timeCommitment':weekItem['timeCommitment'],
                    'week_id':weekItem['id'],
                    'week_slug':weekItem['slug']
                    }
                weekList.append(weekData)
        elif 'sectionTitle' in courseItem[0].keys():
            for weekNum, weekItem in enumerate(courseItem,1):
                if type(weekItem['sectionDetail']) == str:
                    weekData = {
                        'course_id':courseId,
                        'week_num':weekNum,
                        'week_name':weekItem['sectionTitle'],
                        'week_description':weekItem['sectionDetail'],
                        'week_timeCommitment':None,
                        'week_id':None,
                        'week_slug':None
                        }
                    weekList.append(weekData)
                else:
                    weekData = {
                        'course_id':courseId,
                        'week_num':weekNum,
                        'week_name':weekItem['sectionTitle'],
                        'week_description':' '.join(weekItem['sectionDetail']),
                        'week_timeCommitment':None,
                        'week_id':None,
                        'week_slug':None
                        }
                    weekList.append(weekData)
    
    # Create language nodes
    
#    for language in languages:
    for dicts in weekList:
        session.run('CREATE (w:weekSection) SET w = {dict_param}', parameters={'dict_param':dicts})
    session.close()
    
    return weekList


# print('Weeks added were: ', add_weekSection(driver))
    
#pprint(add_weekSection(driver))
print(add_weekSection(driver)[0]['week_name'])