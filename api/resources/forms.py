from wtforms import Form, StringField, SelectField
 
class CourseSearchForm(Form):
    choices = [('Course', 'Course'),
               ('Author', 'Author'),
               ('Language', 'Language')]
    select = SelectField('Search for courses:', choices=choices)
    search = StringField('')
    
class SearchForm(Form):
    search = StringField('')