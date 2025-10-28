from abc import ABC, abstractmethod
from typing import List
from course_management.interactors.dtos import UserTopicCompletionPercentageDTO

class UserTopicProgressStorageInterface(ABC):

    @abstractmethod
    def create_user_topic_progress(self, user_id: str, topic_id: str, percentage: int) -> UserTopicCompletionPercentageDTO:
        pass

    @abstractmethod
    def update_user_topic_progress(self, user_id: str, topic_id: str, percentage: int) -> UserTopicCompletionPercentageDTO:
        pass

    @abstractmethod
    def get_user_topic_progresses(self, user_id: str, topic_ids: List[str]) -> List[UserTopicCompletionPercentageDTO]:
        pass
