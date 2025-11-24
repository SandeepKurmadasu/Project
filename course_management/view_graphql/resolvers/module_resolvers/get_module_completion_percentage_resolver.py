from course_management.exceptions.custom_exceptions import UserNotFound, \
    DBNotFoundedModuleIds
from course_management.interactors.modules.get_user_module_completion_percentage import \
    GetUserModuleCompletionPercentageInteractor
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType, \
    ModuleIdsNotFoundInDBType
from course_management.view_graphql.types.types import \
    GetModuleCompletionPercentageType



def get_module_completion_percentage_resolver(root,info,params):
    module_id = params.module_id
    user_id = params.user_id

    user_storage = UserStorage()
    module_storage = ModuleStorage()
    topic_storage = TopicStorage()
    enrollment_storage = EnrollmentStorage()
    user_learning_path_storage = UserLearningPathStorage()
    user_learning_unit_storage = UserLearningUnitStorage()

    interactor = GetUserModuleCompletionPercentageInteractor(
        user_storage=user_storage,
        module_storage=module_storage,
        topic_storage=topic_storage,
        enrollment_storage=enrollment_storage,
        user_learning_path_storage=user_learning_path_storage,
        user_learning_unit_storage=user_learning_unit_storage
    )

    try:
        result = interactor.get_user_module_completion_percentage(
            user_id=user_id,
            module_id=module_id
        )

        return GetModuleCompletionPercentageType(
            user_id=user_id,
            module_id=module_id,
            percentage=result.percentage,
        )

    except UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)

    except DBNotFoundedModuleIds as e:
        return ModuleIdsNotFoundInDBType(module_ids=e.module_ids)