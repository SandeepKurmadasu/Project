import graphene

from course_management.exceptions.custom_exceptions import (
    UserNotFound,
    CourseNotFound,
    CourseInProgressException,
)

from course_management.interactors.enrollment.enrollment_interactor import EnrollmentInteractor
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.storages.user_learning_unit_storage import UserLearningUnitStorage
from course_management.storages.user_storage import UserStorage
from course_management.storages.course_storage import CourseStorage
from course_management.storages.user_learning_path_storage import UserLearningPathStorage
from course_management.storages.learning_path_storage import LearningPathStorage
from course_management.storages.learning_unit_storage import LearningUnitStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage
from course_management.view_graphql.types.input_types import \
    CreateEnrollmentReqParams
from course_management.view_graphql.types.response_type import \
    CreateEnrollmentResponse

from course_management.view_graphql.types.types import EnrollmentType
from course_management.view_graphql.types.error_types import (
    UserNotFoundType,
    CourseNotFoundType,
    CourseInProgressExceptionType,
)

class EnrollUserForCourse(graphene.Mutation):
    class Arguments:
        params = CreateEnrollmentReqParams(required=True)

    Output = CreateEnrollmentResponse

    @staticmethod
    def mutate(root, info, params):
        user_id = params.user_id
        course_id = params.course_id

        interactor = EnrollmentInteractor(
            enrollment_storage=EnrollmentStorage(),
            user_storage=UserStorage(),
            course_storage=CourseStorage(),
            user_learning_path_storage=UserLearningPathStorage(),
            learning_path_storage=LearningPathStorage(),
            module_storage=ModuleStorage(),
            topic_storage=TopicStorage(),
            learning_unit_storage=LearningUnitStorage(),
            user_learning_unit_storage=UserLearningUnitStorage()
        )

        try:
            result = interactor.enroll_user_in_course(
                user_id=user_id,
                course_id=course_id
            )

            return EnrollmentType(
                id=result.id,
                user_id=result.user_id,
                course_id=result.course_id,
                course_status=result.course_status,
                course_percentage=result.course_percentage,
                user_learning_path_id=result.user_learning_path_id
            )

        except UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)

        except CourseNotFound as e:
            return CourseNotFoundType(course_id=e.course_id)

        except CourseInProgressException as e:
            return CourseInProgressExceptionType(user_id=e.user_id)
