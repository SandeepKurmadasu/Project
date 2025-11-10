from course_management.exceptions.custom_exceptions import \
    UserNotEnrolledCourse
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UserCourseCompletionPercentageDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class GetUserCourseCompletionPercentageInteractor(ValidationMixIn):

    def __init__(self, enrollment_storage: EnrollmentStorageInterface,
                 user_storage: UserStorageInterface,
                 course_storage: CourseStorageInterface,
                 user_learning_path_storage: UserLearningPathStorageInterface):
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage
        self.course_storage = course_storage
        self.user_learning_path_storage = user_learning_path_storage

    def get_user_course_completion_percentage(self, course_id: str,
                                              user_id: str) -> UserCourseCompletionPercentageDTO:
        self.user_storage.check_user_exists(user_id=user_id)
        self.course_storage.check_course_exists(course_id=course_id)
        self._check_user_course_enrollment(user_id=user_id,
                                           course_id=course_id)

        course_completion_percentage = self.calculate_user_course_completion_percentage(
            course_id=course_id,
            user_id=user_id)
        self.enrollment_storage.update_course_percentage(user_id=user_id,
                                                         course_id=course_id,
                                                         percentage=course_completion_percentage)

        return UserCourseCompletionPercentageDTO(
            user_id=user_id,
            course_id=course_id,
            percentage=course_completion_percentage
        )

    def _check_user_course_enrollment(self, user_id: str, course_id: str):
        is_user_enrolled = self.enrollment_storage.check_user_course_enrollment_exist(
            course_id=course_id,
            user_id=user_id)

        if not is_user_enrolled:
            raise UserNotEnrolledCourse(user_id=user_id)

    def calculate_user_course_completion_percentage(self, course_id: str,
                                                    user_id: str) -> int:
        user_learning_progress = self.user_learning_path_storage.get_user_learning_path(
            user_id=user_id,
            course_id=course_id)
        return user_learning_progress.overall_percentage
