from course_management.exceptions.custom_exceptions import NotExistingTopicTypesFound, \
    NotExistingTopicIdsFound, NotExistedTopicFound
from course_management.interactors.validation import ValidationMixIns
from course_management.interactors.dtos import TopicDTO, CreateTopicDTO, \
    UserTopicCompletionPercentageDTO
from course_management.interactors.storage_interface.topic_storage_interface import \
    TopicStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface


class CreateTopicInteractor(ValidationMixIns):

    def __init__(self, topic_storage: TopicStorageInterface, user_storage: UserStorageInterface):
        self.topic_storage = topic_storage
        self.user_storage = user_storage

    def create_topics(self, topics: list[CreateTopicDTO]) -> TopicDTO:
        topic_types = [obj.topic_type for obj in topics]
        self._check_topic_types(topic_types=topic_types)

        return self.topic_storage.create_topics(topics=topics)

    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:
        topic_ids = [obj.topic_id for obj in topics]
        topic_types = [obj.topic_type for obj in topics]

        self._check_valid_topic_ids(topic_ids=topic_ids)
        self._check_topic_types(topic_types=topic_types)

        return self.topic_storage.update_topics(topics=topics)

    def get_topics(self, topic_ids: list[str]) -> list[TopicDTO]:
        self._check_valid_topic_ids(topic_ids=topic_ids)

        return self.topic_storage.get_topics_with_topic_ids(topic_ids=topic_ids)

    def get_user_topic_completion_percentage(self, user_id: str, topic_id: str) -> UserTopicCompletionPercentageDTO:
        self.check_for_user_exists(user_id=user_id, user_storage=self.user_storage)
        self._validate_topic_ids(topic_id=topic_id)

        pass

    def _check_topic_types(self, topic_types: list[str]):
        existing_topic_types = self.topic_storage.get_topic_types()

        not_existed_topic_types = [each_topic_type for each_topic_type in topic_types if
                                   not each_topic_type in existing_topic_types]

        if not_existed_topic_types:
            raise NotExistingTopicTypesFound(topic_types=not_existed_topic_types)

    def _check_valid_topic_ids(self, topic_ids: list[str]):
        existing_topics = self.topic_storage.get_topics_with_topic_ids(topic_ids=topic_ids)
        existing_topic_ids = [obj.topic_id for obj in existing_topics]

        not_existed_topic_ids = [each_topic_id for each_topic_id in topic_ids if
                                 not each_topic_id in existing_topic_ids]

        if not_existed_topic_ids:
            raise NotExistingTopicIdsFound(topic_ids=not_existed_topic_ids)

    def _validate_topic_ids(self, topic_id: str):
        is_existed_topic_id = self.topic_storage.check_topic_exists(topic_id=topic_id)

        if not is_existed_topic_id:
            raise NotExistedTopicFound(topic_id=topic_id)