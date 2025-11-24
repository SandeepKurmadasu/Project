from assessment.exceptions.custom_exceptions import AttemptIdNotFound
from assessment.interactors.attempts_interactor.get_attempt_progress_interactor import \
    GetAttemptProgressInteractor
from assessment.storages.attempt_storage import AttemptStorage
from assessment.view_graphql.types.error_types import AttemptNotFoundType
from assessment.view_graphql.types.types import AssessmentAttemptProgressType


def get_attempt_progress_resolver(root,info,params):
    attempt_id = params.attempt_id

    attempt_storage = AttemptStorage()
    interactor = GetAttemptProgressInteractor(attempt_storage=attempt_storage)

    try:

        result = interactor.get_attempt_progress(attempt_id=attempt_id)

        return AssessmentAttemptProgressType(
            attempt_id=result.attempt_id,
            user_id=result.user_id,
            assessment_id=result.assessment_id,
            total_points=result.total_points,
            status=result.status
        )

    except AttemptIdNotFound as e:
        return AttemptNotFoundType(attempt_id=e.attempt_id)