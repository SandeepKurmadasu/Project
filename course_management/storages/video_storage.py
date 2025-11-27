from course_management.exceptions.custom_exceptions import TopicIdNotFound
from course_management.interactors.dtos import VideoDTO
from course_management.interactors.storage_interfaces.video_storage_interface import VideoStorageInterface
from course_management.models import Video


class VideoStorage(VideoStorageInterface):

    def get_video_by_topic_id(self, topic_id: str) ->VideoDTO:
        try:
            video = Video.objects.get(topic_id=topic_id)
            return VideoDTO(
                video_id=str(video.video_id),
                title=video.title,
                topic_id=str(video.topic_id),
                video_url=video.video_url
            )
        
        except Video.DoesNotExist:
            raise TopicIdNotFound(topic_id=topic_id)
