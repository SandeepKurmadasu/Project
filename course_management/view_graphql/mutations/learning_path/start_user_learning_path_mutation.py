import graphene

from course_management.exceptions.custom_exceptions import \
    LearningPathIdNotFound, UserNotFound, CourseNotFound
from course_management.interactors.learning_path.start_user_course_learning_path import \
    StartUserCourseLearningPathInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.learning_path_storage import \
    LearningPathStorage
from course_management.storages.learning_unit_storage import \
    LearningUnitStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import \
    UserNotFoundType, CourseNotFoundType
from course_management.view_graphql.types.input_types import \
    StartUserLearningPathReqParams
from course_management.view_graphql.types.response_type import \
    UserLearningPathResponse
from course_management.view_graphql.types.types import UserLearningPathType


class StartUserLearningPathMutation(graphene.Mutation):
    class Arguments:
        params = StartUserLearningPathReqParams(required=True)

    Output = UserLearningPathResponse

    @staticmethod
    def mutate(root, info, params):
        user_id = params.user_id
        course_id = params.course_id

        learning_path_storage = LearningPathStorage()
        learning_unit_storage = LearningUnitStorage()
        user_learning_storage = UserLearningPathStorage()
        user_learning_unit_storage = UserLearningUnitStorage()
        user_storage = UserStorage()
        course_storage = CourseStorage()
        module_storage = ModuleStorage()
        topic_storage = TopicStorage()

        interactor = StartUserCourseLearningPathInteractor(
            learning_path_storage=learning_path_storage,
            user_storage=user_storage,
            user_learning_storage=user_learning_storage,
            learning_unit_storage=learning_unit_storage,
            user_learning_unit_storage=user_learning_unit_storage,
            course_storage=course_storage,
            module_storage=module_storage,
            topic_storage=topic_storage
        )

        try:
            user_learning_path_dto = interactor.start_user_course_learning_path(
                user_id=user_id,
                course_id=course_id
            )

            return UserLearningPathType(
                user_learning_path_id=user_learning_path_dto.user_learning_path_id,
                user_id=user_learning_path_dto.user_id,
                learning_path_id=user_learning_path_dto.learning_path_id,
                current_learning_unit_id=user_learning_path_dto.current_learning_unit_id,
                overall_percentage=user_learning_path_dto.overall_percentage,
                status=user_learning_path_dto.status,
            )

        except UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)

        except CourseNotFound as e:
            return CourseNotFoundType(
                course_id=e.course_id
            )
