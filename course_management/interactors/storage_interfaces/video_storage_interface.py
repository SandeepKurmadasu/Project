from abc import ABC, abstractmethod

from course_management.interactors.dtos import VideoDTO


class VideoStorageInterface(ABC):
    @abstractmethod
    def get_video_by_topic_id(self, topic_id: str) ->VideoDTO:
        pass
    