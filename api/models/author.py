from scripts.app_helpers import get_db, close_db


class Author:
    def __init__(self, name=''):
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

    def find_all(self, page=0, page_size=20):
        db = get_db()

        authors = db.run(
            f"MATCH (a:Author) RETURN a SKIP {page} LIMIT {page_size}"
        ).records()

        close_db()

        # TODO: Please find a better way to format this. Or encapsulate behind a function.
        authors = list(map(lambda x: dict(x[0].items()), authors))

        return authors if len(authors) >= 1 else None
