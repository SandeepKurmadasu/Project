from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.interactors.enrollment.enrollment_interactor import \
    EnrollmentInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.storages.learning_path_storage import \
    LearningPathStorage
from course_management.storages.learning_unit_storage import \
    LearningUnitStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage
from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType
from course_management.view_graphql.types.types import EnrollmentType, \
    EnrollmentListType


def get_uer_enrolled_courses_resolver(root,info,params):
    user_id = params.user_id

    interactor = EnrollmentInteractor(
        enrollment_storage=EnrollmentStorage(),
        user_storage=UserStorage(),
        course_storage=CourseStorage(),
        user_learning_path_storage=UserLearningPathStorage(),
        learning_path_storage=LearningPathStorage(),
        module_storage=ModuleStorage(),
        topic_storage=TopicStorage(),
        learning_unit_storage=LearningUnitStorage()
    )

    try:
        results = interactor.get_user_enrolled_courses(user_id=user_id)

        output_data = [EnrollmentType(
                id=result.id,
                user_id=result.user_id,
                course_id=result.course_id,
                course_status=result.course_status,
                course_percentage=result.course_percentage,
                user_learning_path_id=result.user_learning_path_id
            )for result in results]
        return EnrollmentListType(enrollments=output_data)


    except UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)