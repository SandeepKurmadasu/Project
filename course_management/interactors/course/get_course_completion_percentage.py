from course_management.exceptions.custom_exceptions import UserNotEnrolledCourse
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import CoursePercentageDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface


class UserCoursesCompletionPercentageInteractor(ValidationMixIns):

    def __init__(self, course_storage: CourseStorageInterface,enrollment_storage : EnrollmentStorageInterface,user_storage : UserStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage

    def get_user_course_completion_percentage(self, course_id : str ,user_id : str) -> CoursePercentageDTO:

        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_if_course_exists(course_id=course_id,course_storage=self.course_storage)
        self._check_user_course_enrollment(user_id=user_id,course_id=course_id)
        pass

    def _check_user_course_enrollment(self,user_id: str, course_id: str):
        is_user_enrolled = self.enrollment_storage.get_user_course_enrollment_exist(course_id=course_id, user_id=user_id)

        if not is_user_enrolled:
            raise UserNotEnrolledCourse(user_id=user_id)
