from scripts.app_helpers import get_db, close_db


class User:
    def __init__(self, id='', username='', name='', age='', university='', password=''):
        self.age = age
        self.id = id
        self.name = name
        self.password = password
        self.university = university
        self.username = username

    def create(self):
        db = get_db()

        user = {
            'age': self.age,
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'university': self.university,
            'username': self.username
        }

        user = db.run('CREATE (a:Author $user) RETURN a', user=user)

        close_db()

        return user.value()[0]
    
    def check_password(self, username, password):
        db = get_db()
        
        query = db.run(f'MATCH (u:User) WHERE u.username="{username}" AND u.password="{password}" RETURN COUNT(u)').records()
        
        for item in query:
        
            if item[0] == 1:
                result = True
            else:
                result = False
            
        close_db()
        
        return result
    
    def find_history(self, username, page=0, page_size=20):
        db = get_db()
        
        query = db.run(f'MATCH (a:Author)-[:TEACHES]->(c:Course)<-[e:ENROLLED]-(u:User),\
            (c:Course)-[:RELATED_TO]->(k:Knowledge),\
            (c:Course)-[:CONDUCTED_IN]->(l:Language),\
            (c:Course)-[:PROVIDED_BY]->(p:Provider)\
            WHERE u.username = "{username}"\
            RETURN c.course_id, c.description, c.title, c.photo_link, c.direct_link,\
            collect(DISTINCT a.author) as authors, collect(DISTINCT k.knowledge) as tags,\
            l.language, p.provider, e.enrollment_date, e.completion_date, e.status SKIP {page} LIMIT {page_size}')
        
        result_array = []
        for item in query:
            result_array += [{
                    "course_id": item[0],
                    "description": item[1],
                    "title": item[2],
                    "photo_link": item[3],
                    "direct_link": item[4],
                    "authors": item[5],
                    "tags": item[6],
                    "language": item[7],
                    "provider": item[8],
                    "enrollment_date": item[9],
                    "completion_date": item[10],
                    "status": item[11]
                }]
        
        close_db()

        return result_array