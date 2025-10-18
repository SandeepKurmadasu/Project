from course_management.tests import CreateCourseRequestDTO, CourseDTO, CourseValidator


class CreateCourseInteractor:

    def __init__(self,course_storage:CreateCourseInterface):
        self.course_storage=course_storage

    def bulk_create_courses(self,requests : List[CreateCourseRequestDTO]) -> List[CourseDTO]:

        for request in requests:
            self.validate_course_data(
                name=request.name,
                description=request.description
            )
        courses=self.course_storage.bulk_create_courses(courses=requests)
        return courses

    @staticmethod
    def _validate_course_data(self,name:str,description:str):
        CourseValidator.validate_course_data(name,description)
