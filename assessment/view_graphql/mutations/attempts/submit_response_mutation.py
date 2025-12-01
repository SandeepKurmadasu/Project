import graphene

from assessment.exceptions.custom_exceptions import AlreadyAttemptedExist
from assessment.interactors.attempts_interactor.submit_question import \
    SubmitQuestionInteractor
from assessment.interactors.dtos import SubmitResponseDTO
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.storages.attempt_question_submission import \
    AttemptQuestionSubmissionStorage
from assessment.storages.attempt_storage import AttemptStorage
from assessment.storages.question_storage import QuestionStorage
from assessment.view_graphql.types.error_types import AlreadyAttemptedExistType
from assessment.view_graphql.types.input_types import SubmitQuestionReqParams
from assessment.view_graphql.types.response_types import SubmitAnswerResponse
from assessment.view_graphql.types.types import AssessmentAttemptType, \
    SubmitAnswerType


class SubmitResponseMutation(graphene.Mutation):
    class Arguments:
        params = SubmitQuestionReqParams(required=True)

    Output = SubmitAnswerResponse

    @staticmethod
    def mutate(root,info,params):
        input_data = SubmitResponseDTO(
            assessment_id=params.assessment_id,
            attempt_id=params.attempt_id,
            question_id=params.question_id,
            response=params.response
        )

        interactor = SubmitQuestionInteractor(
            question_storage=QuestionStorage(),
            attempt_storage=AttemptStorage(),
            question_response_storage=AttemptQuestionSubmissionStorage(),
            assessment_storage=AssessmentStorage()
        )
        try:
            result = interactor.submit_question_response(input_data)

            return SubmitAnswerType(
                attempt_id=result.attempt_id,
                user_id=result.user_id,
                assessment_id=result.assessment_id,
                total_points=result.total_points,
                is_correct=result.is_correct.value,
                points=result.points
            )
        except AlreadyAttemptedExist as e:
            return AlreadyAttemptedExistType(question_id=e.question_id)
