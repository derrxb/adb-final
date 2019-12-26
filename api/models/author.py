from scripts.app_helpers import get_db, close_db


class Author:
    def __init__(self, name=None):
        self.name = name

    def find_by_id(self, id):
        db = get_db()

        author = db.run(
            "MATCH (a:Author) WHERE ID(a) = $id RETURN a", id=int(id)).single()

        close_db()

        return dict(author.value()) if author != None else None

    def add_author(self, name):
        db = get_db()

        results = db.run("CREATE (a:Author {name: $name})", name=name)

        print(results)

        close_db()

        return results
