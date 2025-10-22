from course_management.interactors.validations import \
    ValidationMixIns
from course_management.interactors.dtos import CourseDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface


class GetCoursesInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        self.check_duplicate_course_ids(course_ids=course_ids)
        self.check_for_db_existed_course_ids(course_ids=course_ids, course_storage=self.course_storage)

        return self.course_storage.get_courses(course_ids=course_ids)
