import graphene

from course_management.view_graphql.types.input_types import GetTopicsParams
from course_management.view_graphql.types.types import TopicType,TopicsType
from course_management.view_graphql.types.error_types import NotExistingTopicTypes, TopicIdsNotFound
from course_management.view_graphql.types.response_type import GetTopicsResponse
from course_management.interactors.topic.topic_interactor import TopicsInteractor
from course_management.storages.topic_storage import TopicStorage
from course_management.exceptions.custom_exceptions import NotExistingTopicIdsFound, NotExistingTopicTypesFound
from course_management.storages.user_learning_unit_storage import UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage


def resolve_get_topics(root,info,params):
    try:
        dtos = TopicsInteractor(topic_storage=TopicStorage(),user_storage=UserStorage(),user_learning_unit_storage=UserLearningUnitStorage()).get_topics(params.topic_ids)
        topics = [
            TopicType(
                module_id=d.module_id,
                title=d.title,
                description=d.description,
                topic_type=d.topic_type,
                content=d.content,
                estimated_duration_in_mins=d.estimate_duration_in_mins
            )
            for d in dtos
        ]
        return TopicsType(topics=topics)


    except NotExistingTopicIdsFound as e:
        return TopicIdsNotFound(topic_ids=e.topic_ids)


    except NotExistingTopicTypesFound as e:
        return NotExistingTopicTypes(topic_types=e.topic_types)

