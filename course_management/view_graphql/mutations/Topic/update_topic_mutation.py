import graphene

from course_management.exceptions import custom_exceptions
from course_management.interactors.dtos import TopicDTO, TopicTypeEnum
from course_management.interactors.topic.topic_interactor import \
    TopicsInteractor
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import \
    NotExistingTopicTypesFoundType, \
    NotExistedTopicFoundType
from course_management.view_graphql.types.input_types import \
    UpdateTopicsReqParams
from course_management.view_graphql.types.response_type import \
    UpdateTopicResponse
from course_management.view_graphql.types.types import TopicGQLType, \
    TopicsListType


class UpdateTopicsMutation(graphene.Mutation):
    class Arguments:
        params = UpdateTopicsReqParams(required=True)

    Output = UpdateTopicResponse

    @staticmethod
    def mutate(root, info, params):
        update_topics = params.topics

        update_data = [
            TopicDTO(
                topic_id=topic.topic_id,
                module_id=topic.module_id,
                title=topic.topic_title,
                description=topic.description,
                topic_type=TopicTypeEnum(topic.topic_type),
                content=topic.content,
                order=topic.order,
                estimate_duration_in_mins=topic.estimated_duration_in_mins
            )
            for topic in update_topics
        ]

        topic_storage = TopicStorage()
        user_storage = UserStorage()
        user_learning_unit_storage = UserLearningUnitStorage()

        interactor = TopicsInteractor(topic_storage=topic_storage,
                                      user_storage=user_storage,
                                      user_learning_unit_storage=user_learning_unit_storage)

        try:

            updated_topics = interactor.update_topics(topics=update_data)

            topics_output = [
                TopicGQLType(
                    topic_id=t.topic_id,
                    module_id=t.module_id,
                    topic_title=t.title,
                    description=t.description,
                    topic_type=t.topic_type,
                    content=t.content,
                    order=t.order,
                    estimated_duration_in_mins=t.estimate_duration_in_mins
                )
                for t in updated_topics
            ]

            return TopicsListType(topics=topics_output)



        except custom_exceptions.NotExistingTopicIdsFound as e:
            return NotExistedTopicFoundType(topic_ids=e.topic_ids)

        except custom_exceptions.NotExistingTopicTypesFound as e:
            return NotExistingTopicTypesFoundType(topic_types=e.topic_types)
