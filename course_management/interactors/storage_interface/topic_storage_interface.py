from abc import ABC, abstractmethod

from course_management.interactors.dtos import CreateTopicDTO, TopicDTO, UserTopicCompletionPercentageDTO

class TopicStorageInterface(ABC):

    @abstractmethod
    def create_topics(self,topics : list[CreateTopicDTO])->TopicDTO:
        pass

    @abstractmethod
    def update_topics(self,topics : list[TopicDTO])->list[TopicDTO]:
        pass

    @abstractmethod
    def get_topics_for_topic_ids(self,topic_ids : list[str])->list[TopicDTO]:
        pass

    @abstractmethod
    def check_topic_exists(self,topic_id : str)->bool:
        pass

    @abstractmethod
    def get_topics_for_module_ids(self,module_ids : list[str])->list[TopicDTO]:
        pass

    @abstractmethod
    def get_user_topic_progresses(self, user_id: str, topic_ids: list[str]) -> list[UserTopicCompletionPercentageDTO]:
        pass

