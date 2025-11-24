from course_management.exceptions.custom_exceptions import UserNotFound, \
    CourseNotFound
from course_management.interactors.learning_path.get_user_learning_path_details import \
    GetUserLearningPathDetailsInteractor
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.view_graphql.types.error_types import UserNotFoundType, \
    CourseNotFoundType
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
        user_learning_path_data = interactor.get_current_learning_unit_status(user_learning_path_id=user_learning_path_id)

        result = UserCurrentLearningUnitStatusType(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_learning_path_data.user_learning_unit_id,
            percentage =user_learning_path_data.percentage,
            status=user_learning_path_data.status
        )
        return result

    except UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)

    except CourseNotFound as e:
        return CourseNotFoundType(
            course_id=e.course_id
        )
