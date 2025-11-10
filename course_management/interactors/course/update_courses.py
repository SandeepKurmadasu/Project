from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CourseDTO, \
    UpdateCourseDTO
from course_management.interactors.storage_interfaces.course_feedback_storage_interface import \
    CourseFeedbackStorageInterface
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface


class UpdateCoursesInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface,
                 feedback_storage: CourseFeedbackStorageInterface):
        self.course_storage = course_storage
        self.feedback_storage = feedback_storage

    def update_courses(self, courses: list[UpdateCourseDTO]) -> \
            list[CourseDTO]:
        course_ids = [obj.course_id for obj in courses]
        course_types = [
            obj.level.value if hasattr(obj.level, "value") else obj.level
            for obj in courses
        ]
        course_titles = [obj.title for obj in courses]
        self.check_duplicate_course_titles(course_titles=course_titles)
        self.check_duplicate_course_ids(course_ids=course_ids)
        self.check_existing_titles(courses=courses,
                                   course_storage=self.course_storage)
        self.check_invalid_level_type(course_types=course_types)

        self.check_course_ids_exist_in_db(course_ids=course_ids,
                                          course_storage=self.course_storage)

        return self.course_storage.update_courses(courses=courses)
