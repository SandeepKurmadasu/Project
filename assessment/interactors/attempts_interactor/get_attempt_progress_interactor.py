""" Create the get attempt progress interactor """
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import \
    AssessmentAttemptProgressDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface


class GetAttemptProgressInteractor(AssessmentValidationMixIn):
    """ Get the attempt progress in this interactor """

    def __init__(self, assessment_attempt_storage: AttemptStorageInterface):
        self.assessment_attempt_storage = assessment_attempt_storage

    def get_attempt_progress(self,
                             attempt_id: str) -> AssessmentAttemptProgressDTO:
        """ Get the user attempt progress"""

        self.validate_attempt_exists(attempt_id=attempt_id,
                                     attempt_storage=self.assessment_attempt_storage)

        return self.assessment_attempt_storage.get_assessment_progress(
            attempt_id=attempt_id)
