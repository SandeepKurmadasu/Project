from course_management.exceptions.custom_exceptions import \
    UserNotEnrolledInModule, LearningPathNotFound
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UserModuleCompletionPercentageDTO
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
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


class GetUserModuleCompletionPercentageInteractor(ValidationMixIn):

    def __init__(self, user_storage: UserStorageInterface,
                 module_storage: ModuleStorageInterface,
                 topic_storage: TopicStorageInterface,
                 enrollment_storage: EnrollmentStorageInterface,
                 user_learning_path_storage: UserLearningPathStorageInterface,
                 user_learning_unit_storage: UserLearningUnitStorageInterface):
        self.user_storage = user_storage
        self.module_storage = module_storage
        self.topic_storage = topic_storage
        self.enrollment_storage = enrollment_storage
        self.user_learning_path_storage = user_learning_path_storage
        self.user_learning_unit_storage = user_learning_unit_storage

    def get_user_module_completion_percentage(self, user_id: str,
                                              module_id: str) -> UserModuleCompletionPercentageDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_modules_exist_in_db(module_ids=[module_id],
                                       module_storage=self.module_storage)
        course_id = self._is_module_enrolled(user_id=user_id,
                                             module_id=module_id)

        self._user_learning_exists(user_id=user_id, course_id=course_id)

        module_percentage = self.calculate_user_module_completion_percentage(
            user_id=user_id, module_id=module_id)

        result = UserModuleCompletionPercentageDTO(
            user_id=user_id,
            module_id=module_id,
            percentage=module_percentage
        )
        return result

    def _user_learning_exists(self, user_id: str, course_id: str):
        learning_path = self.user_learning_path_storage.get_user_learning_path(
            user_id=user_id, course_id=course_id)
        if not learning_path:
            raise LearningPathNotFound(course_id=course_id)

    def calculate_user_module_completion_percentage(self, user_id: str,
                                                    module_id: str) -> int:
        module_topics = self.topic_storage.get_topics_by_module_ids(
            [module_id])
        topic_ids = [obj.topic_id for obj in module_topics]

        user_learning_units_data = self.user_learning_unit_storage.get_learning_units_by_topic_ids(
            user_id=user_id,
            topic_ids=topic_ids)

        if not user_learning_units_data:
            return 0

        total_topics_percentage = sum(
            [obj.percentage for obj in user_learning_units_data])
        module_completion_percentage = int(
            total_topics_percentage / len(topic_ids))

        return module_completion_percentage

    def _is_module_enrolled(self, user_id: str, module_id: str):
        module_data = self.module_storage.get_modules(module_ids=[module_id])
        course_id = module_data[0].course_id

        course_modules = self.enrollment_storage.check_user_course_enrollment_exist(
            course_id=course_id,
            user_id=user_id)

        if not course_modules:
            raise UserNotEnrolledInModule(user_id=user_id)

        return course_id
