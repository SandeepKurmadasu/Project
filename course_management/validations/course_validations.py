from course_management.exceptions.course_exceptions import InvalidCourseIds, InvalidCourseData
from typing import List

class CourseValidator:

    @staticmethod
    def validate_course_ids(course_ids : List[str]):

        invalid_ids=[]
        for course_id in course_ids:
            if not course_id or course_id.strip() == "":
                invalid_ids.append(course_id)

        if invalid_ids:
            raise InvalidCourseIds(course_ids=invalid_ids)

    @staticmethod
    def validate_course_data(name:str,description:str):
        invalid_fields=[]

        if not name or name.strip() == "":
            invalid_fields.append("name")

        if not description or description.strip() == "":
            invalid_fields.append("description")

        if invalid_fields:
            raise InvalidCourseData(invalid_fields=invalid_fields)

    @staticmethod
    def validate_bulk_course_data(requests):
        if not requests:
            raise ValueError("No courses provided for creation.")

        for request in requests:
            CourseValidator.validate_course_data(request.name, request.description)



