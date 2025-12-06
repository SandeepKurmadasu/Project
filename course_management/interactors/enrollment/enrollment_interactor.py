from course_management.exceptions.custom_exceptions import \
    CourseInProgressException
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import EnrollmentDTO, \
    EnrollmentStatusEnum
from course_management.interactors.learning_path.start_user_course_learning_path import \
    StartUserCourseLearningPathInteractor
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.learning_path_storage_interface import \
    LearningPathStorageInterface
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import \
    LearningUnitStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class EnrollmentInteractor(ValidationMixIn):

    def __init__(self,
                 enrollment_storage: EnrollmentStorageInterface,
                 user_storage: UserStorageInterface,
                 course_storage: CourseStorageInterface,
                 user_learning_path_storage: UserLearningPathStorageInterface,
                 learning_path_storage: LearningPathStorageInterface,
                 module_storage: ModuleStorageInterface,
                 topic_storage: TopicStorageInterface,
                 learning_unit_storage: LearningUnitStorageInterface,
                 user_learning_unit_storage: UserLearningUnitStorageInterface):

        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage
        self.course_storage = course_storage
        self.user_learning_path_storage = user_learning_path_storage
        self.learning_path_storage = learning_path_storage
        self.module_storage = module_storage
        self.topic_storage = topic_storage
        self.learning_unit_storage = learning_unit_storage
        self.user_learning_unit_storage = user_learning_unit_storage

    def enroll_user_in_course(self, user_id: str,
                              course_id: str) -> EnrollmentDTO:

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)

        enroll_exist = self.enrollment_storage.check_user_course_enrollment_exist(
            user_id=user_id, course_id=course_id)

        if enroll_exist:

            is_enrolled = self.enrollment_storage.get_enrollment(
                user_id=user_id,
                course_id=course_id
            )
            if is_enrolled:
                if is_enrolled.course_status != EnrollmentStatusEnum.FAIL:
                    return EnrollmentDTO(
                        id=is_enrolled.id,
                        user_id=user_id,
                        course_id=course_id,
                        course_title=is_enrolled.course_title,
                        course_status=is_enrolled.course_status,
                        course_percentage=is_enrolled.course_percentage,
                        user_learning_path_id=is_enrolled.user_learning_path_id
                    )
                self._is_eligible_to_re_enroll_course(
                    user_id=user_id,
                    course_id=course_id
                )

        course_learning_path = self.learning_path_storage.get_latest_learning_path_by_course_id(
            course_id=course_id
        )

        user_leaning_path_interactor = StartUserCourseLearningPathInteractor(
            user_storage=self.user_storage, course_storage=self.course_storage,
            module_storage=self.module_storage,
            topic_storage=self.topic_storage,
            learning_path_storage=self.learning_path_storage,
            learning_unit_storage=self.learning_unit_storage,
            user_learning_storage=self.user_learning_path_storage,
            user_learning_unit_storage=self.user_learning_unit_storage)

        if course_learning_path is None:


            user_learning_path = user_leaning_path_interactor.start_user_course_learning_path(
                user_id=user_id, course_id=course_id)
        else:
            user_learning_path = user_leaning_path_interactor.start_user_course_learning_path(
                user_id=user_id, course_id=course_id)

        user_learning_path_id = user_learning_path.user_learning_path_id

        return self.enrollment_storage.create_enrollment(
            user_id=user_id,
            course_id=course_id,
            user_learning_path_id=user_learning_path_id
        )

    def get_user_enrolled_courses(self, user_id: str) -> list[EnrollmentDTO]:

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.enrollment_storage.get_user_enrolled_courses(
            user_id=user_id)

    def _is_eligible_to_re_enroll_course(self, user_id: str,
                                         course_id: str) -> None:
        enrollment_details = self.enrollment_storage.get_enrollment(
            user_id=user_id,
            course_id=course_id)
        if enrollment_details.course_status != EnrollmentStatusEnum.FAIL:
            raise CourseInProgressException(user_id=user_id)
