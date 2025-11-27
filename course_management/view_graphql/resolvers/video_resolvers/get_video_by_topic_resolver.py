from course_management.interactors.video.get_video_by_topic_id_interactor import GetVideoByTopicIdInteractor
from course_management.storages.video_storage import VideoStorage
from course_management.exceptions.custom_exceptions import TopicIdNotFound
from course_management.view_graphql.types.types import VideoType
from course_management.view_graphql.types.error_types import TopicIdNotFoundType


def resolve_get_video(root, info, params):
    try:
        dto = GetVideoByTopicIdInteractor(
            video_storage=VideoStorage()
        ).execute(params.topic_id)

        return VideoType(
            video_id=dto.video_id,
            title=dto.title,
            topic_id=dto.topic_id,
            video_url=dto.video_url
        )

    except TopicIdNotFound as e:
        return TopicIdNotFoundType(topic_id=e.topic_id)
