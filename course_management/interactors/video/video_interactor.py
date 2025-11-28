from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import TopicVideoDTO
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.interactors.storage_interfaces.video_storage_interface import \
    VideoStorageInterface


class VideoInteractor(ValidationMixIn):

    def __init__(self,video_storage: VideoStorageInterface, topic_storage: TopicStorageInterface):
        self.topic_storage = topic_storage
        self.video_storage = video_storage


    def get_topic_video(self,topic_id: str)-> TopicVideoDTO:
        self.check_topic_exists(topic_id=topic_id,topic_storage=self.topic_storage)

        return self.video_storage.get_topic_video(topic_id=topic_id)