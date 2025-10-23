from course_management.exceptions.custom_exceptions import NotExistingTopicIdsFound
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import UserTopicCompletionPercentageDTO, StatusType
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface


class GetTopicCompletionInteractor(ValidationMixIns):

    def __init__(self, topic_storage: TopicStorageInterface, user_storage: UserStorageInterface):
        self.topic_storage = topic_storage
        self.user_storage = user_storage

    def get_user_topic_completion_percentages(
        self, user_id: str, topic_ids: list[str]
    ) -> list[UserTopicCompletionPercentageDTO]:

        # Validate user exists
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)

        # Validate all topic IDs exist
        existing_topics = self.topic_storage.get_topics_for_topic_ids(topic_ids=topic_ids)
        existing_topic_ids = [t.topic_id for t in existing_topics]
        invalid_topic_ids = [tid for tid in topic_ids if tid not in existing_topic_ids]
        if invalid_topic_ids:
            raise NotExistingTopicIdsFound(topic_ids=invalid_topic_ids)

        # Fetch all user topic progresses in bulk
        user_progress_list = self.topic_storage.get_user_topic_progresses(user_id=user_id, topic_ids=topic_ids)
        progress_map = {p.topic_id: p for p in user_progress_list}

        # For topics not started, return percentage=0 and status=LEARNING
        result = []
        for tid in topic_ids:
            if tid in progress_map:
                result.append(progress_map[tid])
            else:
                result.append(UserTopicCompletionPercentageDTO(
                    user_id=user_id,
                    topic_id=tid,
                    status=StatusType.LEARNING.value,
                    percentage=0
                ))
        return result