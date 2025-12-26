from assessment.exceptions.custom_exceptions import AttemptIdNotFound
from assessment.interactors.attempts_interactor.get_attempt_score_interactor import \
    GetAttemptScoreInteractor
from assessment.storages.attempt_storage import AttemptStorage
from assessment.view_graphql.types.error_types import AttemptNotFoundType
from assessment.view_graphql.types.types import AttemptScoreType


def get_attempt_score_resolver(root,info,params):
    attempt_id = params.attempt_id

    attempt_storage = AttemptStorage()
    interactor = GetAttemptScoreInteractor(attempt_storage=attempt_storage)

    try:
        result = interactor.get_attempt_score(attempt_id=attempt_id)

        return AttemptScoreType(
            attempt_id=result.attempt_id,
            user_id=result.user_id,
            score=result.score,
            started_at=result.started_at
        )

    except AttemptIdNotFound as e:
        return AttemptNotFoundType(attempt_id=e.attempt_id)