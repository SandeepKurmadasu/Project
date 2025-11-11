"""Interactor for creating the Question Bank"""
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)
from assessment.interactors.dtos import QuestionBankDTO


class CreateQuestionBankInteractor(AssessmentValidationMixIn):
    """Handles logic for creating the question bank"""

    def __init__(self,
                 question_storage: QuestionStorageInterface):  # TODO add the questionBank Storage interface
        self.storage = question_storage

    def create_question_bank(self, name: str,
                             assessment_id: str) -> QuestionBankDTO:
        """
        Create a new question bank after validation.

        Args:
            name: Name of the question bank.
            assessment_id: Assessment for Question Bank
        Returns:
            QuestionBankDTO: Newly created question bank.
        """
        self.check_duplicate_bank_name(name, self.storage)

        return self.storage.create_question_bank(name=name,
                                                 assessment_id=assessment_id)
