"""Create the start assessment attempt interactor """
from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from course_management.tests.interactors.course_tests.test_for_recommended_courses import \
    user_storage


class StartAssessmentAttemptInteractor(ValidationMixIn,
                                       AssessmentValidationMixIn):
    """ Start the user assessment attempt interactor"""

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 user_storage: UserStorageInterface,
                 assessments_storage: AssessmentStorageInterface):
        self.attempt_storage = attempt_storage
        self.user_storage = user_storage
        self.assessments_storage = assessments_storage

    def start_assessment_attempt(self, user_id: str,
                                 assessment_id: str) -> AssessmentAttemptDTO:
        """start the user attempt for assessment """

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.validate_assessment_exists(assessment_id=assessment_id,
                                        assessment_storage=self.assessments_storage)

        return self.attempt_storage.create_assessment_attempt(user_id=user_id,
                                                              assessment_id=assessment_id)
