from course_management.interactors.validation import \
    ValidationMixIns
from course_management.interactors.dtos import CourseDTO, UpdateCourseDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface


class UpdateCoursesInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface):
        self.course_storage = course_storage

    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[CourseDTO]:
        course_ids = [obj.course_id for obj in courses]

        self.check_duplicate_course_ids(course_ids=course_ids)
        self.check_duplicate_course_titles(courses=courses, course_storage=self.course_storage)

        self.check_invalid_level_type(courses=courses, course_storage=self.course_storage)

        self.check_for_db_existed_course_ids(course_ids=course_ids, course_storage=self.course_storage)

        return self.course_storage.update_courses(courses=courses)
