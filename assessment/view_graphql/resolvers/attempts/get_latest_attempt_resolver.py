from assessment.exceptions.custom_exceptions import AssessmentIdNotFound
from assessment.interactors.attempts_interactor.get_latest_attempt_interactor import \
    GetLatestAssessmentAttemptInteractor
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.storages.attempt_storage import AttemptStorage
from assessment.view_graphql.types.error_types import AssessmentNotFoundType
from assessment.view_graphql.types.types import AssessmentAttemptType


def get_latest_attempt_resolver(root,info,params):
    user_id = params.user_id
    assessment_id = params.assessment_id

    assessment_storage = AssessmentStorage()
    attempt_storage = AttemptStorage()

    interactor = GetLatestAssessmentAttemptInteractor(attempt_storage=attempt_storage,assessments_storage=assessment_storage)

    try:
        result = interactor.get_latest_assessment_attempt(user_id=user_id,assessment_id=assessment_id)

        return AssessmentAttemptType(
            attempt_id=result.attempt_id,
            user_id=result.user_id,
            assessment_id = result.assessment_id,
            total_points = result.total_points,
            question_ids = result.question_ids,
            status = result.status,
            started_at = result.started_at
        )

    except AssessmentIdNotFound as e:
        return AssessmentNotFoundType(assessment_id=e.assessment_id)


