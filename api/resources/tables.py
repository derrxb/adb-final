
from flask_table import Table, Col
 
class Results(Table):
    course_id = Col('Course ID', show=False)
    title = Col('Title')
    description = Col('Description')
    direct_link = Col('URL')
    photo_link = Col('Photo URL', show=False)
    authors = Col('Authors')
    tags = Col('Tags')
    language = Col('Language')
    provider = Col('Provider')