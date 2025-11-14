from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CourseDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface


class GetCoursesInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        self.check_duplicate_course_ids(course_ids=course_ids)
        self.check_course_ids_exist_in_db(course_ids=course_ids,
                                          course_storage=self.course_storage)

        return self.course_storage.get_courses(course_ids=course_ids)
