"""End the attempt Interactor"""
from cyber_edu_verse.assessment.interactors.assessment_validations import \
    AssessmentValidationMixIn
from cyber_edu_verse.assessment.interactors.dtos import AssessmentAttemptDTO
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.course_management.interactors.dtos import StatusEnum


class EndAttemptInteractor(AssessmentValidationMixIn):
    """Create the end attempt interactor"""

    def __init__(self, attempt_storage: AttemptStorageInterface):
        self.attempt_storage = attempt_storage

    def end_attempt(self, attempt_id: str) -> AssessmentAttemptDTO:
        """End an attempt user click the end attempt """
        self.validate_attempt_exists(attempt_id=attempt_id,
                                     attempt_storage=self.attempt_storage)

        return self.attempt_storage.end_an_attempt(attempt_id=attempt_id,
                                                   status=StatusEnum.COMPLETE)
