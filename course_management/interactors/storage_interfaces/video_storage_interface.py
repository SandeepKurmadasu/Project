from abc import ABC, abstractmethod

from course_management.interactors.dtos import CreateTopicVideoDTO, \
    TopicVideoDTO


class VideoStorageInterface(ABC):

    @abstractmethod
    def create_topic_video(self, topic_video_data: CreateTopicVideoDTO) -> TopicVideoDTO:
        pass

    @abstractmethod
    def get_topic_video(self,topic_id: str) -> TopicVideoDTO:
        pass