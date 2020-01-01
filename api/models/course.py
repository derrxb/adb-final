from scripts.app_helpers import get_db, close_db


class Course:
    def __init__(self, name=''):
        self.name = name

    def find_all(self, page=0, page_size=20):
        db = get_db()

        courses = db.run(
            f"MATCH (c:Course) RETURN c SKIP {page} LIMIT {page_size}"
        ).records()

        close_db()

        # TODO: Please find a better way to format this. Or encapsulate behind a function.
        courses = list(map(lambda x: dict(x[0].items()), courses))

        return courses if len(courses) >= 1 else None
