import os
from flask import Flask, g, Blueprint, render_template, request, redirect, flash
from flask_restful import Api
from flask_cors import CORS
from .resources.Author import AuthorResource
from .resources.Authors import AuthorsResource
from .resources.Courses import CoursesResource
from api import app
from py2neo import ogm
from flask2neo4j import Flask2Neo4J
from .resources.forms import CourseSearchForm
from .resources.tables import Results

from api.models.course import Course
from api.common.cypher_helpers import page_number, page_size

# Wrap app with API to enable Flask-REST API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(AuthorsResource, '/authors')
api.add_resource(AuthorResource, '/authors/<int:id>')
api.add_resource(CoursesResource, '/courses')
app.register_blueprint(api_bp)

@app.route('/', methods=['GET','POST'])
def index():
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

#@app.route('/results')
def search_results(search):
    results = []
#    search_dim = search.data['select']
    search_string = search.data['search']
 
    if search_string == '':
        results = Course().find_all(page_number(), page_size())
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
    else:
        # display results
        results = Course().find(search_string, page_number(), page_size())
        if not results:
            flash(search_string)
            return render_template('notfound.html')
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
    
    

print(app.url_map)

# Enable debugging mode for dev environments
if __name__ == '__main__':
    app.run(debug=True)
