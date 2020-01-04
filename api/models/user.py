from scripts.app_helpers import get_db, close_db


class User:
    def __init__(self, id='', username='', name='', age='', university=''):
        self.name = name
        self.age = age
        self.university = university

    def create(self):
        db = get_db()

        user = {
            'name': self.name,
            'id': self.id,
            'username': self.username,
            'university': self.university,
            'age': self.age
        }

        user = db.run('CREATE (a:Author $user) RETURN a', user=user)

        close_db()

        return user.value()[0]
