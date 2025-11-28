import graphene
from course_management.view_graphql.types.input_types import CreateTopicsInput
from course_management.view_graphql.types.types import TopicsType, TopicType

from course_management.interactors.topic.topic_interactor import \
    TopicsInteractor, CreateTopicDTO
from course_management.storages.topic_storage import TopicStorage
from course_management.exceptions.custom_exceptions import \
    NotExistingTopicTypesFound

from course_management.view_graphql.types.error_types import \
    NotExistingTopicTypes
from course_management.view_graphql.types.response_type import \
    CreateTopicsResponse
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage


class CreateTopics(graphene.Mutation):
    class Arguments:
        params = graphene.Argument(CreateTopicsInput, required=True)

    Output = CreateTopicsResponse

    @staticmethod
    def mutate(root, info, params):
        from course_management.models import Topic

        try:

            dtos = [
                CreateTopicDTO(
                    module_id=t.module_id,
                    title=t.title,
                    description=t.description,
                    topic_type=Topic.TopicTypeEnum(t.topic_type),
                    content=t.content,
                    order=t.order,
                    estimate_duration_in_mins=t.estimate_duration_in_mins
                )
                for t in params.topics
            ]

            created_topics = TopicsInteractor(topic_storage=TopicStorage(),
                                              user_storage=UserStorage(),
                                              user_learning_unit_storage=UserLearningUnitStorage()).create_topics(
                dtos)

            topic_objs = [
                TopicType(
                    module_id=ct.module_id,
                    title=ct.title,
                    description=ct.description,
                    topic_type=ct.topic_type,
                    content=ct.content,
                    estimated_duration_in_mins=ct.estimate_duration_in_mins
                )
                for ct in created_topics
            ]

            return TopicsType(topics=topic_objs)

        except NotExistingTopicTypesFound as e:
            return NotExistingTopicTypes(topic_types=e.topic_types)
