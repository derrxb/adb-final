from scripts.app_helpers import get_db, close_db
from datetime import date
from scripts.helpers import format_cypher_list


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

    def find_by_username(self, username):
        db = get_db()

        user = format_cypher_list(db.run('''MATCH (u:User) WHERE u.username = $username RETURN u''',
                                         username=username))

        close_db()

        return user

    def check_password(self, username, password):
        db = get_db()
        query = db.run(
            f'MATCH (u:User) WHERE u.username="{username}" AND u.password="{password}" RETURN COUNT(u)').records()

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
              (c:Course)-[:CONDUCTED_IN]->(l:Language),\
              (c:Course)-[:PROVIDED_BY]->(p:Provider)\
              WHERE (u.username = "{username}")\
              RETURN c.course_id, c.description, c.title, c.photo_link, c.direct_link,\
                     collect(DISTINCT a.author) as authors , l.language, p.provider, \
                     e.enrollment_date, e.completion_date, e.status SKIP {page} LIMIT {page_size}')

        result_array = []
        for item in query:
            result_array += [{
                "course_id": item[0],
                "description": item[1],
                "title": item[2],
                "photo_link": item[3],
                "direct_link": item[4],
                "authors": item[5],
                "language": item[6],
                "provider": item[7],
                "enrollment_date": item[8],
                "completion_date": item[9],
                "status": item[10]
            }]

        close_db()

        return result_array

    def enroll_in_course(self, username, course_id):
        db = get_db()

        enrollment = {
            'enrollment_date': date.today(),
            'status': 'IN_PROGRESS',
        }

        query = '''MATCH (c:Course), (u:User)
                   WHERE c.course_id = $course_id AND u.username = $username
                   CREATE(u)-[r:ENROLLED $enrollment] -> (c)
                   RETURN type(r)'''

        result = db.run(query, course_id=course_id,
                        username=username, enrollment=enrollment)

        return True

    def enrolled_in(self, username, course_id):
        """Determines if a user is enrolled in a course already"""
        db = get_db()

        query = '''MATCH (u:User)-[r:ENROLLED]->(c:Course)
                   WHERE c.course_id = $course_id AND u.username = $username
            RETURN r'''

        result = db.run(query, course_id=course_id,
                        username=username).single()

        return True if result != None and len(result) > 0 else False

    def requires_prerequisite(self, username, course_id):
        """Returns boolean indicating if the user needs a prerequisite for this course"""

        db = get_db()

        prerequisites = '''MATCH (c:Course)-[r:REQUIRES]->(c2:Course)
 WHERE c.course_id = $course_id
            RETURN c'''

        prerequisites_results = db.run(
            prerequisites, course_id=course_id).single()

        # If the course has no prereq allow the user to sign up
        if prerequisites_results == None:
            return False

        # If it has prereq ensures they've taken them.
        query = '''MATCH (c:Course)-[r:REQUIRES]->(c2:Course)<-[r2:ENROLLED]-(u:User)
                   WHERE u.username = $username AND r2.status = 'COMPLETE D' AND c.course_id = $course_id
            RETURN c
           '''

        result = db.run(query, course_id=course_id,
                        username=username).single()

        return True if result == None else False

    def find_all(self, page=0, page_size=20):
        db = get_db()

        courses = db.run(
            f"MATCH (u:User)-[e:ENROLLED]->(c:Course)\
            RETURN u.name, collect(DISTINCT c.title) as Courses, collect(DISTINCT c.course_id) as CourseIds, u.username SKIP {page} LIMIT {page_size}"
        ).records()

        result_array = []
        for item in courses:
            result_array += [{
                "user": item[0],
                "courses_taken": item[1],
                "course_id": item[2],
                "username": item[3]
            }]

        close_db()

        return result_array

    def find(self, query='', page=0, page_size=20):
        db = get_db()
        # Problem: search using author, results in author column only output 1 author (keyword)
        # and not multiple, if there are any.
        courses = db.run(
            f'MATCH (u:User)-[e:ENROLLED]->(c:Course) WHERE (u.name =~ ".*(?i){query}.*")\
            RETURN u.name, collect(DISTINCT c.title) as Courses, collect(DISTINCT c.course_id) as CourseIds, u.username  SKIP {page} LIMIT {page_size}'
        ).records()

        result_array = []
        for item in courses:
            result_array += [{
                "user": item[0],
                "courses_taken": item[1], # '; '.join(item[1]),
                "course_id": item[2],
                "username": item[3]
            }]

        print(result_array)
        close_db()

        return result_array
