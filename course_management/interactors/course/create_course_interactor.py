from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CreateCourseDTO, \
    CourseDTO, LevelEnum, CourseCategoryEnum
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface


class CreateCoursesInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[
        CourseDTO]:

        for c in courses:
            if isinstance(c.level, str):
                c.level = LevelEnum(c.level)
            if isinstance(c.category, str):
                c.category = CourseCategoryEnum(c.category)

        course_level_types = [c.level for c in courses]
        course_titles = [c.title for c in courses]

        self.check_duplicate_course_titles(course_titles=course_titles)
        self.check_existing_titles(courses=courses,
                                   course_storage=self.course_storage)
        self.check_invalid_level_type(course_level_types=course_level_types)

        return self.course_storage.create_courses(courses)
