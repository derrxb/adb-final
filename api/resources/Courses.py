from flask_restful import Resource, abort
from flask import request
from api.models.course import Course
from api.common.cypher_helpers import page_number, page_size


class CoursesResource(Resource):
    """Endpoint for courses"""

    def get(self):
        courses = Course().find_all(page_number(), page_size())

        if courses == None:
            abort(404, error="No courses found")

        return courses
