from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.dtos import CourseDTO

class GetRecommendCoursesInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface,enrollment_storage: EnrollmentStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage

    def get_recommended_courses(self, user_id: str) -> list[CourseDTO]:
        user_enrolled_course_ids = self.enrollment_storage.get_user_enrolled_courses(user_id=user_id)

        return self.course_storage.get_recommend_courses(course_ids=user_enrolled_course_ids)
