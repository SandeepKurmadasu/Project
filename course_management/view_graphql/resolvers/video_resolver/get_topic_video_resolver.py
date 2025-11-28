from course_management.exceptions.custom_exceptions import NotExistedTopicFound
from course_management.interactors.video.video_interactor import \
    VideoInteractor
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.video_storage import VideoStorage
from course_management.view_graphql.types.error_types import TopicNotFound
from course_management.view_graphql.types.types import TopicVideoType


def get_topic_video_resolver(root,info,params):
    topic_id = params.topic_id

    topic_storage = TopicStorage()
    video_storage = VideoStorage()

    interactor = VideoInteractor(topic_storage=topic_storage,video_storage=video_storage)

    try:
        result = interactor.get_topic_video(topic_id=topic_id)

        return TopicVideoType(
            video_id=result.video_id,
            title = result.title,
            topic_id=result.topic_id,
            video_url=result.video_url
        )

    except NotExistedTopicFound as e:
        return TopicNotFound(topic_id=e.topic_id)