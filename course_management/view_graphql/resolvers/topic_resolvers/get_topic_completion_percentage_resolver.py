from course_management.exceptions.custom_exceptions import (
    NotExistedTopicFound,UserNotFound
)
from course_management.interactors.topic.topic_interactor import \
    TopicsInteractor
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.user_learning_unit_storage import UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage

from course_management.view_graphql.types.error_types import (
    NotExistedTopicFoundType,
    UserNotFoundType,
)
from course_management.view_graphql.types.types import \
    GetTopicCompletionPercentageType


def get_user_topic_completion_percentage(root, info, params):
    user_id = params.user_id
    topic_id = params.topic_id

    user_storage = UserStorage()
    topic_storage = TopicStorage()
    user_learning_unit_storage = UserLearningUnitStorage()

    interactor = TopicsInteractor(
        topic_storage=topic_storage,
        user_storage=user_storage,
        user_learning_unit_storage=user_learning_unit_storage,
    )

    try:
        result = interactor.get_user_topic_completion_percentage(
            user_id=user_id,
            topic_id=topic_id
        )

        return GetTopicCompletionPercentageType(
            user_id=result.user_id,
            topic_id=result.topic_id,
            percentage=result.percentage,
        )

    except UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)

    except NotExistedTopicFound as e:
        return NotExistedTopicFoundType(topic_id=e.topic_id)
