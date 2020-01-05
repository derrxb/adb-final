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
    
    # use a set to avoid duplicates
    allauthors = set()

    for authors in data['Author'].values():
        if type(authors)is list:
            if authors: #if list is not empty
                for person in authors:
                    if person != "":
                        allauthors.add(person)
        else:
            if authors != "":
                allauthors.add(authors)

    # print authors
    # for x in allauthors:
    #    print(x)

    allauthors = list(allauthors)

    # Load to neo4j
    for names in allauthors:
        session.run('CREATE (a:Author {author: $author }) RETURN a', author=names)

        
    
    session.close()
    
    return len(allauthors)

if __name__ == '__main__':
    print("Authors added",add_author(driver))
