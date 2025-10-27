from course_management.interactors.dtos import UserModuleCompletionPercentageDTO
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface
from course_management.interactors.validations import ValidationMixIns


class GetUserModuleCompletionPercentageInteractor(ValidationMixIns):

    def __init__(self,user_storage : UserStorageInterface,module_storage : ModuleStorageInterface,topic_storage: TopicStorageInterface):
        self.user_storage = user_storage
        self.module_storage = module_storage
        self.topic_storage=topic_storage

    def get_user_module_completion_percentage(self, user_id: str, module_id: str) -> UserModuleCompletionPercentageDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_modules_in_db(module_ids=[module_id], module_storage=self.module_storage)

        module_percentage = self.calculate_user_module_completion_percentage(user_id=user_id, module_id=module_id)

        result = UserModuleCompletionPercentageDTO(
            user_id=user_id,
            module_id=module_id,
            percentage=module_percentage
        )
        return result

    def calculate_user_module_completion_percentage(self, user_id: str, module_id: str) -> int:
        module_topics = self.topic_storage.get_topics_for_module_ids([module_id])
        topic_ids = [obj.topic_id for obj in module_topics]
        attempted_topics = self.topic_storage.get_user_topic_progresses(user_id=user_id, topic_ids=topic_ids)

        if not attempted_topics:
            return 0

        total_topics_percentage = sum([obj.percentage for obj in attempted_topics])
        module_completion_percentage = int(total_topics_percentage / len(topic_ids))

        return module_completion_percentage

