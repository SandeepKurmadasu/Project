from course_management.exceptions.custom_exceptions import UserNotFound, \
    CourseNotFound, LearningUnitIdNotFound, UserLearningPathNotFound
from course_management.interactors.learning_path.get_user_learning_path_details import \
    GetUserLearningPathDetailsInteractor
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.view_graphql.types.error_types import UserNotFoundType, \
    CourseNotFoundType, LearningUnitIdNotFoundType, \
    UserLearningPathNotFoundType
from course_management.view_graphql.types.types import \
    UserCurrentLearningUnitStatusType


def get_user_current_learning_unit_status_resolver(root, info, params):
    user_learning_path_id = params.user_learning_path_id

    user_learning_storage = UserLearningPathStorage()
    user_learning_unit_storage = UserLearningUnitStorage()

    interactor = GetUserLearningPathDetailsInteractor(
        user_learning_path_storage=user_learning_storage,
        user_learning_unit_storage=user_learning_unit_storage)

    try:
        user_learning_path_data = interactor.get_current_learning_unit_status(
            user_learning_path_id=user_learning_path_id)

        result = UserCurrentLearningUnitStatusType(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_learning_path_data.user_learning_unit_id,
            percentage=user_learning_path_data.percentage,
            status=user_learning_path_data.status
        )
        return result

    except LearningUnitIdNotFound as e:
        return LearningUnitIdNotFoundType(learning_unit_id=e.learning_unit_id)

    except UserLearningPathNotFound as e:
        return UserLearningPathNotFoundType(
            user_learning_path_id=e.user_learning_path_id
        )
