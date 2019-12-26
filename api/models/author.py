from scripts.app_helpers import get_db, close_db


class Author:
    def __init__(self, name):
        self.name = name

    def add_author(self, name):
        db = get_db()

        results = db.run("CREATE (a:Author {name: $name})", name=name)

        print(results)

        close_db()

        return results
