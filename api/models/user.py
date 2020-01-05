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
