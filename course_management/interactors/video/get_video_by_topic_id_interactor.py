from course_management.interactors.dtos import VideoDTO
from course_management.storages.video_storage import VideoStorage


class GetVideoByTopicIdInteractor:
    def __init__(self, video_storage: VideoStorage):
        self.video_storage = video_storage

    def execute(self, topic_id: str) -> VideoDTO:
        """
        Retrieve the video associated with the given topic_id.

        Args:
            topic_id (str): The topic identifier

        Returns:
            VideoDTO: The video data associated with the topic

        Raises:
            TopicIdNotFound: If no video is found for the specified topic_id
        """
        return self.video_storage.get_video_by_topic_id(topic_id)
