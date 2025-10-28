from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.dtos import CourseDTO

class GetRecommendCoursesInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface,enrollment_storage: EnrollmentStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage

    def get_recommended_courses(self, user_id: str) -> list[CourseDTO]:
        self.check_valid_user_id(user_id)
        user_enrolled_course_ids = self.enrollment_storage.get_user_enrolled_courses(user_id=user_id)
        all_course_ids = self.course_storage.get_all_course_ids()

        remaining_course_ids = [course_id for course_id in all_course_ids
                                if course_id not in user_enrolled_course_ids]

        return self.course_storage.get_courses(course_ids=remaining_course_ids)

