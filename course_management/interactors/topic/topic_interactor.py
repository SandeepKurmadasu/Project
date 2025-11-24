from course_management.exceptions.custom_exceptions import \
    NotExistingTopicTypesFound, \
    NotExistingTopicIdsFound, NotExistedTopicFound
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import TopicDTO, \
    CreateTopicDTO, \
    UserTopicCompletionPercentageDTO, TopicTypeEnum
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class TopicsInteractor(ValidationMixIn):

    def __init__(self, topic_storage: TopicStorageInterface,
                 user_storage: UserStorageInterface,
                 user_learning_unit_storage: UserLearningUnitStorageInterface):
        self.topic_storage = topic_storage
        self.user_storage = user_storage
        self.user_learning_unit_storage = user_learning_unit_storage

    def create_topics(self, topics: list[CreateTopicDTO]) -> list[TopicDTO]:
        topic_types = [obj.topic_type.value for obj in topics]

        self._check_topic_types(topic_types=topic_types)

        return self.topic_storage.create_topics(topics=topics)

    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:
        topic_ids = [obj.topic_id for obj in topics]
        topic_types = [obj.topic_type.value for obj in topics]

        self._check_valid_topic_ids(topic_ids=topic_ids)
        self._check_topic_types(topic_types=topic_types)

        return self.topic_storage.update_topics(topics=topics)

    def get_topics(self, topic_ids: list[str]) -> list[TopicDTO]:
        self._check_valid_topic_ids(topic_ids=topic_ids)

        return self.topic_storage.get_topics_by_topic_ids(topic_ids=topic_ids)

    def get_user_topic_completion_percentage(self, user_id: str,
                                             topic_id: str) -> UserTopicCompletionPercentageDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self._validate_topic_id(topic_id=topic_id)

        topic_percentage = self.user_topic_attempt_percentage(
            topic_id=topic_id,
            user_id=user_id)

        result = UserTopicCompletionPercentageDTO(
            user_id=user_id,
            topic_id=topic_id,
            percentage=topic_percentage
        )
        return result

    @staticmethod
    def _check_topic_types(topic_types: list[str]):
        existing_topic_types = [each_topic_types.value for each_topic_types in
                                TopicTypeEnum]

        not_existed_topic_types = [each_topic_type for each_topic_type in
                                   topic_types if
                                   each_topic_type not in existing_topic_types]

        if not_existed_topic_types:
            raise NotExistingTopicTypesFound(
                topic_types=not_existed_topic_types)

    def _check_valid_topic_ids(self, topic_ids: list[str]):

        existing_topics = self.topic_storage.get_topics_by_topic_ids(
            topic_ids=topic_ids)
        existing_topic_ids = [obj.topic_id for obj in existing_topics]

        not_existed_topic_ids = [each_topic_id for each_topic_id in topic_ids
                                 if
                                 each_topic_id not in existing_topic_ids]

        if not_existed_topic_ids:
            raise NotExistingTopicIdsFound(topic_ids=not_existed_topic_ids)

    def _validate_topic_id(self, topic_id: str):
        is_existed_topic_id = self.topic_storage.check_topic_exists(
            topic_id=topic_id)

        if not is_existed_topic_id:
            raise NotExistedTopicFound(topic_id=topic_id)

    def user_topic_attempt_percentage(self, topic_id: str, user_id: str):
        topic_data = self.user_learning_unit_storage.get_learning_units_by_topic_ids(
            user_id=user_id, topic_ids=[topic_id])
        if not topic_data:
            return 0
        return topic_data[0].percentage
