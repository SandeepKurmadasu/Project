from assessment.exceptions import custom_exceptions
from course_management.exceptions.custom_exceptions import CourseNotFound, \
    UserNotFound
from course_management.interactors.course.get_user_course_completion_percentage import \
    GetUserCourseCompletionPercentageInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType, \
    CourseNotFoundType
from course_management.view_graphql.types.types import \
    GetUserCourseCompletionPercentageType


def get_user_course_completion_percentage(root, info, params):
    course_id = params.course_id
    user_id = params.user_id

    enrollment_storage = EnrollmentStorage()
    user_storage = UserStorage()
    course_storage = CourseStorage()
    user_learning_path_storage = UserLearningPathStorage()

    interactor = GetUserCourseCompletionPercentageInteractor(
        user_storage=user_storage, course_storage=course_storage,
        enrollment_storage=enrollment_storage,
        user_learning_path_storage=user_learning_path_storage)

    try:
        result = interactor.get_user_course_completion_percentage(user_id=user_id,course_id=course_id)

        return GetUserCourseCompletionPercentageType(
            user_id=result.user_id,
            course_id=result.course_id,
            percentage=result.percentage
        )

    except UserNotFound as e:
        return UserNotFoundType(
            user_id=e.user_id
        )

    except CourseNotFound as e:
        return CourseNotFoundType(
            course_id=e.course_id
        )


