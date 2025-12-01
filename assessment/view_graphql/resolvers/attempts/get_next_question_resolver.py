from assessment.exceptions.custom_exceptions import AttemptIdNotFound
from assessment.interactors.attempts_interactor.get_next_question_interactor import \
    GetNextQuestionInteractor
from assessment.interactors.dtos import DisplayQuestionDTO, \
    AssessmentAttemptProgressDTO
from assessment.storages.attempt_question_submission import \
    AttemptQuestionSubmissionStorage
from assessment.storages.attempt_storage import AttemptStorage
from assessment.storages.question_storage import QuestionStorage
from assessment.view_graphql.types.error_types import AttemptNotFoundType
from assessment.view_graphql.types.types import DisplayQuestionType, \
    AssessmentAttemptProgressType


def get_next_question_resolver(root, info, params):
    attempt_id = params.attempt_id

    attempt_storage = AttemptStorage()
    question_storage = QuestionStorage()
    response_question_storage = AttemptQuestionSubmissionStorage()

    interactor = GetNextQuestionInteractor(attempt_storage=attempt_storage,
                                           question_storage=question_storage,
                                           response_question_storage=response_question_storage)

    try:
        result = interactor.get_next_question(attempt_id=attempt_id)

        if isinstance(result,DisplayQuestionDTO):
            return DisplayQuestionType(
                question_id=result.question_id,
                question_text=result.question_text,
                question_type=result.question_type.value,
                options=result.options
            )

        if isinstance(result,AssessmentAttemptProgressDTO):
            return AssessmentAttemptProgressType(
                attempt_id=result.attempt_id,
                user_id=result.user_id,
                assessment_id=result.assessment_id,
                total_points=result.total_points,
                status=result.status
            )
    except AttemptIdNotFound as e:
        return AttemptNotFoundType(attempt_id=e.attempt_id)
