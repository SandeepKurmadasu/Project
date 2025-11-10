from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CourseDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class GetRecommendCoursesInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface,
                 enrollment_storage: EnrollmentStorageInterface,
                 user_storage: UserStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage

    def get_recommended_courses(self, user_id: str) -> list[CourseDTO]:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        user_enrolled_courses = self.enrollment_storage.get_user_enrolled_courses(
            user_id=user_id)
        course_ids = [obj.course_id for obj in user_enrolled_courses]
        all_courses = self.course_storage.get_all_courses()
        recommended_course_ids = [each_course.course_id for each_course in
                                  all_courses if
                                  each_course.course_id not in course_ids]

        return self.course_storage.get_courses(
            course_ids=recommended_course_ids)
