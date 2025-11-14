from course_management.exceptions.custom_exceptions import \
    CourseInProgressException
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import EnrollmentDTO, \
    EnrollmentStatusEnum
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class EnrollmentInteractor(ValidationMixIn):

    def __init__(self, enrollment_storage: EnrollmentStorageInterface,
                 user_storage: UserStorageInterface,
                 course_storage: CourseStorageInterface,
                 user_learning_path_storage: UserLearningPathStorageInterface):
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage
        self.course_storage = course_storage
        self.user_learning_path_storage = user_learning_path_storage

    def enroll_user_in_course(self, user_id: str, user_learning_path_id: str,
                              course_id: str) -> EnrollmentDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)
        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_path_storage)
        is_enrolled_course = self.enrollment_storage.check_user_course_enrollment_exist(
            user_id=user_id,
            course_id=course_id)
        if is_enrolled_course:
            self._is_eligible_to_re_enroll_course(user_id=user_id,
                                                  course_id=course_id)

        return self.enrollment_storage.create_enrollment(user_id=user_id,
                                                         course_id=course_id)

    def get_user_enrolled_courses(self, user_id: str) -> list[EnrollmentDTO]:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.enrollment_storage.get_user_enrolled_courses(
            user_id=user_id)

    def _is_eligible_to_re_enroll_course(self, user_id: str, course_id: str):
        enrollment_details = self.enrollment_storage.get_enrollment(
            user_id=user_id,
            course_id=course_id)

        if enrollment_details is None:
            return

        if enrollment_details.course_status != EnrollmentStatusEnum.FAIL:
            raise CourseInProgressException(user_id=user_id)
