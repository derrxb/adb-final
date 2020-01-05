
from flask_table import Table, Col
 
class Results(Table):
	# classes = ['table', 'table-bordered', 'table-striped']
	photo_link = Col('Photo URL', show=False)
	course_id = Col('Course ID', show=False)
	title = Col('Title')
	description = Col('Description')
	direct_link = Col('URL')
	authors = Col('Authors')
	tags = Col('Tags')
	language = Col('Language')
	provider = Col('Provider')
    
class History(Table):
    # classes = ['table', 'table-bordered', 'table-striped']
    photo_link = Col('Photo URL', show=False)
    course_id = Col('Course ID', show=False)
    title = Col('Title')
    description = Col('Description')
    direct_link = Col('URL')
    authors = Col('Authors')
    tags = Col('Tags')
    language = Col('Language')
    provider = Col('Provider')
    enrollment_date = Col('Enrollment Date')
    completion_date = Col('Completion Date')
    status = Col('Status')