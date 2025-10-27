from course_management.exceptions.custom_exceptions import NotExistingTopicIdsFound, NotExistedTopicFound
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import TopicDTO, CreateTopicDTO, UserTopicCompletionPercentageDTO
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface


class TopicInteractor(ValidationMixIns):

    def __init__(self, topic_storage: TopicStorageInterface, user_storage: UserStorageInterface):
        self.topic_storage = topic_storage
        self.user_storage = user_storage

    def create_topics(self, topics: list[CreateTopicDTO]) -> TopicDTO:
        return self.topic_storage.create_topics(topics=topics)

    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:
        topic_ids = [obj.topic_id for obj in topics]
        self._check_valid_topic_ids(topic_ids=topic_ids)
        return self.topic_storage.update_topics(topics=topics)

    def get_topics(self, topic_ids: list[str]) -> list[TopicDTO]:
        self._check_valid_topic_ids(topic_ids=topic_ids)
        return self.topic_storage.get_topics_for_topic_ids(topic_ids=topic_ids)


    def get_user_topic_completion_percentage(self, user_id: str, topic_id: str) -> UserTopicCompletionPercentageDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self._validate_topic_id(topic_id=topic_id)

        topic_percentage = self.user_topic_attempt_percentage(topic_id=topic_id, user_id=user_id)

        result = UserTopicCompletionPercentageDTO(
            user_id=user_id,
            topic_id=topic_id,
            percentage=topic_percentage
        )
        return result


    def _check_valid_topic_ids(self, topic_ids: list[str]):
        existing_topics = self.topic_storage.get_topics_for_topic_ids(topic_ids=topic_ids)
        existing_topic_ids = [obj.topic_id for obj in existing_topics]

        not_existed_topic_ids = [each_topic_id for each_topic_id in topic_ids if
                                 each_topic_id not in existing_topic_ids]

        if not_existed_topic_ids:
            raise NotExistingTopicIdsFound(topic_ids=not_existed_topic_ids)

    def _validate_topic_id(self, topic_id: str):
        is_existed_topic_id = self.topic_storage.check_topic_exists(topic_id=topic_id)

        if not is_existed_topic_id:
            raise NotExistedTopicFound(topic_id=topic_id)

    def user_topic_attempt_percentage(self, topic_id: str, user_id: str):
        topic_percentage = self.topic_storage.get_user_topic_progresses(user_id=user_id, topic_ids=[topic_id])

        return topic_percentage[0].percentage