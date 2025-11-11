from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import Algorithm, AssessmentAttemptDTO, \
    QuestionDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class StartAssessmentAttemptInteractor(ValidationMixIn,
                                       AssessmentValidationMixIn):
    """Start the user assessment attempt interactor"""

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 user_storage: UserStorageInterface,
                 assessments_storage: AssessmentStorageInterface,
                 question_bank_storage: QuestionStorageInterface):
        self.attempt_storage = attempt_storage
        self.user_storage = user_storage
        self.assessments_storage = assessments_storage
        self.question_bank_storage = question_bank_storage

    def start_assessment_attempt(self, user_id: str, assessment_id: str,
                                 question_selection: Algorithm) -> AssessmentAttemptDTO:
        """Start the user attempt for assessment"""

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.validate_assessment_exists(assessment_id=assessment_id,
                                        assessment_storage=self.assessments_storage)

        assessment_data = self.assessments_storage.get_assessment(
            assessment_id=assessment_id)

        bank_id = assessment_data.assessment_question_bank.bank_id

        questions = self.get_next_n_questions(user_id=user_id,
                                              bank_id=bank_id,
                                              question_selection=question_selection,
                                              assessment_id=assessment_id,
                                              n=assessment_data.no_of_questions)
        question_ids = [obj.question_id for obj in questions]

        return self.attempt_storage.create_assessment_attempt(
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=question_ids)


    def get_next_n_questions(self, user_id: str, question_selection: Algorithm,
                             assessment_id: str, n: int, bank_id: str) -> list[
        QuestionDTO]:
        """Get next N questions skipping already attempted (for random/difficulty)."""

        previously_attempted_questions = self.attempt_storage.get_assessment_attempted_questions(
            user_id=user_id,
            assessment_id=assessment_id)

        previously_attempted_question_ids = [obj.question_id for obj in
                                             previously_attempted_questions]

        if question_selection == Algorithm.FIXED:
            fixed_questions = self.question_bank_storage.get_question_bank_questions(
                bank_id=bank_id, limit=n)
            return fixed_questions[:n]

        get_question_selection = [] # got list question ids

        return get_question_selection







