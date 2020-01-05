from scripts.app_helpers import get_db, close_db


class Course:
    def __init__(self, name=''):
        self.name = name

    def find_all(self, page=0, page_size=20):
        db = get_db()

        courses = db.run(
            f"MATCH (a:Author)-[:TEACHES]->(c:Course)-[:RELATED_TO]->(k:Knowledge),\
            (c:Course)-[:CONDUCTED_IN]->(l:Language), (c:Course)-[:PROVIDED_BY]->(p:Provider)\
            RETURN c.course_id, c.description, c.title, c.photo_link, c.direct_link,\
            collect(DISTINCT a.author) as authors, collect(DISTINCT k.knowledge) as tags,\
            l.language, p.provider SKIP {page} LIMIT {page_size}"
        ).records()

        result_array = []
        for item in courses:
            result_array += [{
                "course_id": item[0],
                "description": item[1],
                "title": item[2],
                "photo_link": item[3],
                "direct_link": item[4],
                "authors": item[5],
                "tags": item[6],
                "language": item[7],
                "provider": item[8]
            }]

        close_db()

        return result_array

    def find(self, query='', page=0, page_size=20):
        db = get_db()
        # Problem: search using author, results in author column only output 1 author (keyword)
        # and not multiple, if there are any.
        courses = db.run(
            f'MATCH (a:Author)-[:TEACHES]->(c:Course)-[:RELATED_TO]->(k:Knowledge),\
                (c:Course)-[:CONDUCTED_IN]->(l:Language), (c:Course)-[:PROVIDED_BY]->(p:Provider)\
                WHERE (c.description =~ ".*(?i){query}.*" OR c.title =~".*(?i){query}.*"\
                OR a.author =~ ".*(?i){query}.*" OR k.knowledge =~ ".*(?i){query}.*")\
                RETURN c.course_id, c.description, c.title, c.photo_link, c.direct_link,\
                collect(DISTINCT a.author) as authors, collect(DISTINCT k.knowledge) as tags,\
                l.language, p.provider SKIP {page} LIMIT {page_size}'
        ).records()

        result_array = []
        for item in courses:
            result_array += [{
                "course_id": item[0],
                "description": item[1],
                "title": item[2],
                "photo_link": item[3],
                "direct_link": item[4],
                "authors": ', '.join(item[5]),
                "tags": ', '.join(item[6]),
                "language": item[7],
                "provider": item[8]
            }]

        close_db()

        return result_array

    def find_by_id(self, id):
        db = get_db()

        # Load and build course using a given course_id
        course = db.run(
            f'MATCH (a:Author)-[:TEACHES]->(c:Course)-[:RELATED_TO]->(k:Knowledge),\
                (c:Course)-[:CONDUCTED_IN]->(l:Language), (c:Course)-[:PROVIDED_BY]->(p:Provider)\
                WHERE c.course_id = $course_id \
                RETURN c.course_id, c.description, c.title, c.photo_link, c.direct_link,\
                collect(DISTINCT a.author) as authors, collect(DISTINCT k.knowledge) as tags,\
                l.language, p.provider', course_id=id
        ).single()

        if course != None:
            formatted_course = {
                "course_id": course[0],
                "description": course[1],
                "title": course[2],
                "photo_link": course[3],
                "direct_link": course[4],
                "authors": ', '.join(course[5]),
                "tags": ', '.join(course[6]),
                "language": course[7],
                "provider": course[8]
            }

            return formatted_course
        else:
            None
