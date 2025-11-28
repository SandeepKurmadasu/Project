import graphene

from course_management.exceptions.custom_exceptions import CourseNotFound, \
    UserNotFound
from course_management.interactors.dtos import CourseFeedbackDTO
from course_management.interactors.feedback.create_course_feedback_interactor import \
    CreateCourseFeedbackInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.feedback_storage import FeedbackStorage
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import \
    CourseNotFoundType, UserNotFoundType
from course_management.view_graphql.types.input_types import \
    FeedbackForCourseReqParams
from course_management.view_graphql.types.response_type import \
    CourseFeedbackResponse
from course_management.view_graphql.types.types import FeedbackType


class FeedbackForCourseMutation(graphene.Mutation):
    class Arguments:
        params = FeedbackForCourseReqParams(required=True)

    Output = CourseFeedbackResponse

    @staticmethod
    def mutate(root, info, params):
        input_data = CourseFeedbackDTO(
            course_id=params.course_id,
            user_id=params.user_id,
            rating=params.rating,
            message=params.message
        )

        course_storage = CourseStorage()
        feedback_storage = FeedbackStorage()
        user_storage = UserStorage()

        interactor = CreateCourseFeedbackInteractor(user_storage=user_storage,
                                                    course_storage=course_storage,
                                                    feedback_storage=feedback_storage)

        try:
            result = interactor.create_course_feedback(
                feedback_data=input_data)

            return FeedbackType(
                course_id=result.course_id,
                user_id=result.user_id,
                rating=result.rating,
                message=result.message
            )

        except CourseNotFound as e:
            return CourseNotFoundType(course_id=e.course_id)

        except UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)
