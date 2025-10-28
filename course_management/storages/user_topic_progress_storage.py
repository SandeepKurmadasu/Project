from course_management.models import UserTopicProgress
from course_management.interactors.storage_interface.user_topic_progress_storage_interface import UserTopicProgressStorageInterface
from course_management.interactors.dtos import UserTopicCompletionPercentageDTO

class UserTopicProgressStorage(UserTopicProgressStorageInterface):
    def create_user_topic_progress(self, user_id: str, topic_id: str,percentage: int) -> UserTopicCompletionPercentageDTO:
        progress = UserTopicProgress.objects.create(
            user_id=user_id,
            topic_id=topic_id,
            percentage=percentage
        )
        return UserTopicCompletionPercentageDTO(
            user_id=progress.user.user_id,
            topic_id=progress.topic.topic_id,
            percentage=progress.percentage
        )

    def update_user_topic_progress(self, user_id: str, topic_id: str,percentage: int) -> UserTopicCompletionPercentageDTO:
        pass


    def get_user_topic_progresses(self, user_id: str, topic_ids: list[str]) -> list[UserTopicCompletionPercentageDTO]:
        progresses = UserTopicProgress.objects.filter(
            user_id=user_id,
            topic_id__in=topic_ids
        )
        return [
            UserTopicCompletionPercentageDTO(
                user_id=progress.user.user_id,
                topic_id=progress.topic.topic_id,
                percentage=progress.percentage
            )
            for progress in progresses
        ]

