from course_management.interactors.dtos import TopicVideoDTO, \
    CreateTopicVideoDTO
from course_management.interactors.storage_interfaces.video_storage_interface import \
    VideoStorageInterface
from course_management.models import Video, Topic


class VideoStorage(VideoStorageInterface):

    def create_topic_video(self, topic_video_data: CreateTopicVideoDTO) -> TopicVideoDTO:
        topic = Topic.objects.get(topic_id=topic_video_data.topic_id)

        topic_video = Video.objects.create(title=topic_video_data.title,
                                           topic=topic,
                                           video_url=topic_video_data.video_url)

        return TopicVideoDTO(
            video_id=topic_video.video_id,
            title=topic_video.title,
            topic_id=topic_video.topic.topic_id,
            video_url=topic_video.video_url
        )

    def get_topic_video(self, topic_id: str) -> TopicVideoDTO:
        video_data = Video.objects.get(topic_id=topic_id)

        return TopicVideoDTO(
            video_id=video_data.video_id,
            title=video_data.title,
            topic_id=video_data.topic.topic_id,
            video_url=video_data.video_url
        )
