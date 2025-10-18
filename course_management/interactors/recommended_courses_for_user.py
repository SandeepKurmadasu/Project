from course_management.interactors.storage_interface.dtos import CourseRecommendationDTO
from course_management.tests import CourseStorageInterface


class RecommendedCoursesForUserInteractor:

        def __init__(self, user_storage: UserStorageInterface, course_storage: CourseStorageInterface):
            self.user_storage = user_storage
            self.course_storage = course_storage

        def recommended_courses_for_user(self,user_id: str, limit:int=5) -> List[CourseRecommendationDTO]:
          pass
