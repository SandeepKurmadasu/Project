"""Interactor for creating the Question Bank"""
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import (
    QuestionBankStorageInterface
)
from assessment.interactors.dtos import QuestionBankDTO


class CreateQuestionBankInteractor(AssessmentValidationMixIn):
    """Handles logic for creating the question bank"""
    def __init__(self, question_bank_storage: QuestionBankStorageInterface,
                 assessment_storage: AssessmentStorageInterface):
        self.question_bank_storage = question_bank_storage
        self.assessment_storage = assessment_storage

    def create_question_bank(self, name: str, assessment_id: str) -> QuestionBankDTO:
        """
        Create a new question bank after validation.

        Args:
            name: Name of the question bank.
            assessment_id: (optional) ID of the assessment to link this bank to.

        Returns:
            QuestionBankDTO: Newly created question bank.
        """
        self.check_duplicate_bank_name(name, self.question_bank_storage)
        self.validate_assessment_exists(assessment_id=assessment_id, assessment_storage=self.assessment_storage)


        return self.question_bank_storage.create_question_bank_for_assessment(
            assessment_id=assessment_id, name=name)
