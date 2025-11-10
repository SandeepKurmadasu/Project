from abc import ABC, abstractmethod

from course_management.interactors.dtos import CreateTopicDTO, \
    TopicDTO


class TopicStorageInterface(ABC):

    @abstractmethod
    def create_topics(self, topics: list[CreateTopicDTO]) -> list[TopicDTO]:
        pass

    @abstractmethod
    def get_topics_by_topic_ids(self, topic_ids: list[str]) -> list[TopicDTO]:
        pass

    @abstractmethod
    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:
        pass

    @abstractmethod
    def check_topic_exists(self, topic_id: str) -> bool:
        pass

    @abstractmethod
    def get_topics_by_module_ids(self, module_ids: list[str]) -> list[
        TopicDTO]:
        pass
