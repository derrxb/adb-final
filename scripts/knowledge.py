import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=('neo4j',  'password'))


def add_knowledge(driver):
    session = driver.session()
    alltags = []
    for courseId, tags in data['Knowledge'].items():

        for tag in tags:
            tag = {
            'course_id': courseId,
            'knowledge': tag
            }
            
            alltags.append(tag)
       

    # Load dictionary to neo4j
    for dicts in alltags:
        session.run('CREATE (k:Knowledge) SET k = {dict_param}', parameters={'dict_param':dicts})
    
    session.close()
    
    return alltags

print("Knowledge added",add_knowledge(driver))
