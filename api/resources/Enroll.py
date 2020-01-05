from flask_restful import Resource, abort
from flask import request
from api.models.course import Course
from api.models.user import User
from api.common.cypher_helpers import page_number, page_size


class EnrollResource(Resource):
    """Endpoint to enroll in a course"""

    def post(self):
        course_id = request.args.get('course_id')
        username = request.args.get('username')

        if course_id == None or username == None:
            abort(401, error="We need both the username and course_id")

        enrolled = User().enrolled_in(username, course_id)

        if enrolled == True:
            abort(403, error="You are already enrolled in this course")

        requires_prerequisite = User().requires_prerequisite(username, course_id)

        if requires_prerequisite == True:
            abort(403, error="This course has a prerequite that you haven't taken")

        print(requires_prerequisite)

        results = User().enroll_in_course(username, course_id)

        # abort(403, error="This courseasdfasdf has a prerequite that you haven't taken")
        return results
