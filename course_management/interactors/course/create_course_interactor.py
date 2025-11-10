from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CreateCourseDTO, \
    CourseDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface


class CreateCoursesInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[
        CourseDTO]:
        course_types = [
            obj.level.value if hasattr(obj.level, "value") else obj.level
            for obj in courses
        ]
        course_titles = [obj.title for obj in courses]
        self.check_duplicate_course_titles(course_titles=course_titles)
        self.check_existing_titles(courses=courses,
                                   course_storage=self.course_storage)

        self.check_invalid_level_type(course_types=course_types)

        return self.course_storage.create_courses(courses=courses)
