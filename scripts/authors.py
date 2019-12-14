import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=('neo4j',  'password'))


def add_author(driver):
    session = driver.session()
    allauthors = []
    for courseId, authors in data['Author'].items():
    
        if type(authors)is list:
            for person in authors:
                author = {
                'course_id': courseId,
                'author': person
                }
                #print (author['course_id'], author['author'])
                allauthors.append(author)
        else:
            if authors != "":
                author = {
                    'course_id': courseId,
                    'author': authors
                }
            #print (author['course_id'], author['author'])
            allauthors.append(author)

    # Load dictionary to neo4j
    for dicts in allauthors:
        session.run('CREATE (a:Author) SET a = {dict_param}', parameters={'dict_param':dicts})
    
    session.close()
    
    return allauthors

print("Authors added",add_author(driver))
