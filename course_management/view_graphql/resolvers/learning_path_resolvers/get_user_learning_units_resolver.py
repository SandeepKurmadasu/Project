from course_management.exceptions.custom_exceptions import \
    UserLearningPathIdNotFound
from course_management.interactors.learning_path.get_user_learning_path_details import \
    GetUserLearningPathDetailsInteractor
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.view_graphql.types.error_types import \
    UserLearningPathIdNotFoundType
from course_management.view_graphql.types.types import \
    UserLearningUnitsProgressType, \
    UserLearningUnitProgressType


def get_user_learning_units_resolver(root, info, params):
    user_learning_path_id = params.user_learning_path_id

    user_learning_storage = UserLearningPathStorage()
    user_learning_unit_storage = UserLearningUnitStorage()

    interactor = GetUserLearningPathDetailsInteractor(
        user_learning_path_storage=user_learning_storage,
        user_learning_unit_storage=user_learning_unit_storage)

    try:
        output_data = interactor.get_user_learning_units(
            user_learning_path_id=user_learning_path_id)

        result = [UserLearningUnitProgressType(
            user_learning_path_id=each.user_learning_path_id,
            user_learning_unit_id=each.user_learning_unit_id,
            topic_id=each.topic_id,
            is_locked=each.is_locked,
            module_id=each.module_id,
            percentage=each.percentage,
            status=each.status
        ) for each in output_data]

        return UserLearningUnitsProgressType(units=result)

    except UserLearningPathIdNotFound as e:
        return UserLearningPathIdNotFoundType(user_learning_path_id=e.user_learning_path_id)
