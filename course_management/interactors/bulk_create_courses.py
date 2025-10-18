from course_management.tests import CreateCourseRequestDTO, CourseDTO, CourseValidator


class CreateCourseInteractor:

    def __init__(self,course_storage:CreateCourseInterface):
        self.course_storage=course_storage

    def bulk_create_courses(self,requests : List[CreateCourseRequestDTO]) -> List[CourseDTO]:
        CourseValidator.validate_bulk_course_data(requests)
        courses=self.course_storage.bulk_create_courses(courses=requests)
        return courses
