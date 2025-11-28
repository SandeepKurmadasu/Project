import graphene

from course_management.exceptions.custom_exceptions import \
    LearningUnitLockedException, UserLearningUnitNotFound
from course_management.interactors.learning_path.update_learning_unit_progress_status import \
    UpdateLearningUnitProgressStatusInteractor

from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.view_graphql.types.error_types import \
    LearningUnitLockedExceptionType, UserLearningUnitIdNotFoundType
from course_management.view_graphql.types.input_types import \
    UpdateLearningUnitProgressInput
from course_management.view_graphql.types.response_type import \
    UpdateLearningUnitProgressResponse
from course_management.view_graphql.types.types import \
    UpdateLearningUnitProgressType


class UpdateLearningUnitProgressMutation(graphene.Mutation):
    class Arguments:
        params = UpdateLearningUnitProgressInput(required=True)

    Output = UpdateLearningUnitProgressResponse

    @staticmethod
    def mutate(root, info, params):
        interactor = UpdateLearningUnitProgressStatusInteractor(
            user_learning_storage=UserLearningPathStorage(),
            user_learning_units_storage=UserLearningUnitStorage(),
        )

        try:
            response_dto = interactor.update_learning_unit_progress_status(
                user_learning_path_id=params.user_learning_path_id,
                user_learning_unit_id=params.user_learning_unit_id,
                status=params.status,
                percentage=params.percentage,
            )

            return UpdateLearningUnitProgressType(
                user_learning_path_id=response_dto.user_learning_path_id,
                user_learning_unit_id=response_dto.user_learning_unit_id,
                updated_status=response_dto.updated_status,
                updated_percentage=response_dto.updated_percentage,
                next_unit_unlocked=response_dto.next_unit_unlocked,
                next_unit_id=response_dto.next_unit_id,
                overall_path_percentage=response_dto.overall_path_percentage,
            )

        except UserLearningUnitNotFound as e:
            return UserLearningUnitIdNotFoundType(
                user_learning_unit_id=e.user_learning_unit_id
            )
        except LearningUnitLockedException as e:
            return LearningUnitLockedExceptionType(
                user_learning_unit_id=e.user_learning_unit_id
            )
