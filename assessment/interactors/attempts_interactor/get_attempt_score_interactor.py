"""Create the get attempt score interactor """
from cyber_edu_verse.assessment.interactors.assessment_validations import \
    AssessmentValidationMixIn
from cyber_edu_verse.assessment.interactors.dtos import AttemptScoreDTO
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface


class GetAttemptScoreInteractor(AssessmentValidationMixIn):
    """ Get the user attempt interactor """

    def __init__(self, attempt_storage: AttemptStorageInterface):
        self.attempt_storage = attempt_storage

    def get_attempt_score(self, attempt_id: str) -> AttemptScoreDTO:
        """ Get the user assessment attempt score  """
        self.validate_attempt_exists(attempt_id=attempt_id,
                                     attempt_storage=self.attempt_storage)

        attempt_data = self.attempt_storage.get_assessment_attempt(
            attempt_id=attempt_id)

        return AttemptScoreDTO(
            attempt_id=attempt_id,
            user_id=attempt_data.user_id,
            score=attempt_data.total_points
        )
