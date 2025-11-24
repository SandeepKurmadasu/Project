import graphene

from assessment.exceptions.custom_exceptions import AssessmentIdNotFound
from assessment.interactors.attempts_interactor.start_assessment_attempt_interactor import \
    StartAssessmentAttemptInteractor
from assessment.interactors.dtos import AttemptsCompletedDTO, \
    AssessmentAttemptDTO
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.storages.attempt_question_submission import \
    AttemptQuestionSubmissionStorage
from assessment.storages.attempt_storage import AttemptStorage
from assessment.storages.question_bank_question_storage import \
    QuestionBankQuestionStorage
from assessment.storages.question_bank_storage import QuestionBankStorage
from assessment.storages.question_storage import QuestionStorage
from assessment.view_graphql.types.error_types import AssessmentNotFoundType, \
    AssessmentUserNotFoundType
from assessment.view_graphql.types.input_types import StartAttemptReqParams
from assessment.view_graphql.types.response_types import \
    StartAttemptResponse  # Import only
from assessment.view_graphql.types.types import AttemptsCompletedType, \
    AssessmentAttemptType
from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.storages.user_storage import UserStorage


class StartAssessmentAttempt(graphene.Mutation):
    class Arguments:
        params = StartAttemptReqParams(required=True)

    Output = StartAttemptResponse  # Use the imported union

    @staticmethod
    def mutate(root, info, params):
        user_id = params.user_id
        assessment_id = params.assessment_id

        interactor = StartAssessmentAttemptInteractor(
            attempt_storage=AttemptStorage(),
            user_storage=UserStorage(),
            assessments_storage=AssessmentStorage(),
            question_storage=QuestionStorage(),
            question_bank_storage=QuestionBankStorage(),
            user_question_submitted_storage=AttemptQuestionSubmissionStorage(),
            question_bank_question_storage=QuestionBankQuestionStorage()
        )

        try:
            result = interactor.start_assessment_attempt(
                user_id=user_id,
                assessment_id=assessment_id
            )

            if isinstance(result, AttemptsCompletedDTO):
                return AttemptsCompletedType(
                    user_id=result.user_id,
                    assessment_id=result.assessment_id,
                    attempts_limit=result.attempts_limit,
                    user_attempted_count=result.user_attempted_count
                )

            if isinstance(result, AssessmentAttemptDTO):
                return AssessmentAttemptType(
                    attempt_id=result.attempt_id,
                    user_id=result.user_id,
                    assessment_id=result.assessment_id,
                    total_points=result.total_points,
                    question_ids=result.question_ids,
                    status=result.status.value,
                    started_at=result.started_at
                )

        except AssessmentIdNotFound as e:
            return AssessmentNotFoundType(assessment_id=e.assessment_id)

        except UserNotFound as e:
            return AssessmentUserNotFoundType(user_id=e.user_id)
