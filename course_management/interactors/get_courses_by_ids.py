from course_management.tests import CourseStorageInterface, CourseDTO, CourseValidator


class GetCoursesByIdsInteractor:

    def __init__(self,course_storage : CourseStorageInterface):
        self.course_storage=course_storage

    def get_courses_by_ids(self,course_ids: List[str]) -> List[CourseDTO]:
        self.validate_course_ids(course_ids=course_ids)
        courses=self.course_storage.get_courses_by_ids(course_ids)
        return courses

    def _validate_course_ids(self,course_ids:List[str]):

        CourseValidator.validate_course_ids(course_ids)
