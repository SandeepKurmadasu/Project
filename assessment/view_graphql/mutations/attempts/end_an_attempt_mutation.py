import graphene

from assessment.exceptions.custom_exceptions import AttemptIdNotFound
from assessment.interactors.attempts_interactor.end_attempt_interactor import \
    EndAttemptInteractor
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.storages.attempt_storage import AttemptStorage
from assessment.view_graphql.types.error_types import AttemptNotFoundType
from assessment.view_graphql.types.input_types import EndAnAttemptReqParams
from assessment.view_graphql.types.response_types import AttemptEndResponse
from assessment.view_graphql.types.types import AttemptEndType
from course_management.storages.enrollment_storage import EnrollmentStorage


class AttemptEndMutation(graphene.Mutation):
    class Arguments:
        params = EndAnAttemptReqParams(required=True)

    Output = AttemptEndResponse

    @staticmethod
    def mutate(root, info, params):
        attempt_id = params.attempt_id

        attempt_storage = AttemptStorage()
        assessment_storage = AssessmentStorage()
        enrollment_storage = EnrollmentStorage()

        interactor = EndAttemptInteractor(attempt_storage=attempt_storage,
                                          assessment_storage=assessment_storage,
                                          enrollment_storage=enrollment_storage)

        try:
            result = interactor.end_attempt(attempt_id=attempt_id)

            return AttemptEndType(
                attempt_id=result.attempt_id,
                user_id=result.user_id,
                assessment_id=result.assessment_id,
                total_points=result.total_points,
                question_ids=result.question_ids,
                status=result.status,
                started_at=result.started_at,
                completed_at=result.completed_at
            )

        except AttemptIdNotFound as e:
            return AttemptNotFoundType(attempt_id=e.attempt_id)
