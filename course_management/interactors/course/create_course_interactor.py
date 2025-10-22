from course_management.interactors.validation import \
    ValidationMixIns
from course_management.interactors.dtos import CourseDTO, CreateCourseDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface


class CreateCoursesInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[CourseDTO]:
        self.check_duplicate_course_titles(courses=courses, course_storage=self.course_storage)
        self.check_invalid_level_type(courses=courses,course_storage=self.course_storage)

        return self.course_storage.create_courses(courses=courses)

