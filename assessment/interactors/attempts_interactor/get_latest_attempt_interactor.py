"""Create the get latest attempt interactor """
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface


class GetLatestAssessmentAttemptInteractor(AssessmentValidationMixIn):
    """Get the user latest assessment interactor """

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 assessments_storage: AssessmentStorageInterface):
        self.attempt_storage = attempt_storage
        self.assessments_storage = assessments_storage

    def get_latest_assessment_attempt(self, user_id: str,
                                      assessment_id: str) -> AssessmentAttemptDTO:
        """ Get the user latest assessment attempt data"""

        self.validate_assessment_exists(assessment_id=assessment_id,
                                        assessment_storage=self.assessments_storage)

        return self.attempt_storage.get_latest_assessment_attempt(
            user_id=user_id,
            assessment_id=assessment_id)
