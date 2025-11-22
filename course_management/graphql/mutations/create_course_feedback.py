from collections import UserString

import graphene

from course_management.exceptions.custom_exceptions import CourseNotFound, UserNotFound
from course_management.graphql.types import CheckCourseFound, CheckUserFound
from course_management.graphql.types.input_types import CreateCourseFeedbackInput
from course_management.graphql.types.response_types import CreateFeedbackResponse
from course_management.graphql.types.types import CourseFeedbackType
from course_management.interactors.dtos import CourseFeedbackDTO
from course_management.interactors.feedback.create_course_feedback_interactor import CreateCourseFeedbackInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.feedback_storage import FeedbackStorage
from course_management.storages.user_storage import UserStorage


class CreateCourseFeedbackMutation(graphene.Mutation):
    class Arguments:
        input = CreateCourseFeedbackInput(required=True)

    Output = CreateFeedbackResponse

    def mutate(self, info, input: CreateCourseFeedbackInput):

        feedback_dto = CourseFeedbackDTO(
            course_id=input.course_id,
            user_id=input.user_id,
            rating=input.rating,
            message=input.message or ""
        )

        interactor = CreateCourseFeedbackInteractor(
            course_storage=CourseStorage(),
            feedback_storage=FeedbackStorage(),
            user_storage=UserStorage()
        )

        try:
            result_dto = interactor.create_course_feedback(feedback_dto)

            return CourseFeedbackType(
                course_id=result_dto.course_id,
                user_id=result_dto.user_id,
                rating=result_dto.rating,
                message=result_dto.message
            )

        except CourseNotFound:
            return CheckCourseFound(course_id=input.course_id)

        except UserNotFound:
            return CheckUserFound(user_id=input.user_id)