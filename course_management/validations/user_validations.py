from course_management.exceptions.user_exceptions import InvalidUserId
from course_management.exceptions.user_exceptions import InvalidCourseId

class UserValidator:

    @staticmethod
    def validate_user_id(self,user_id:str):
        if not user_id or user_id.strip() == "":
            raise InvalidUserId(user_id=user_id)

    @staticmethod
    def validate_course_id(self, course_id: str):
        if not course_id or course_id.strip() == "":
            raise InvalidCourseId(course_id=course_id)
