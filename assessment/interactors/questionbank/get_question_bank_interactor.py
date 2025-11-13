"""Interactor to get the question bank"""
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import (
    QuestionBankStorageInterface
)

class GetQuestionBankInteractor(AssessmentValidationMixIn):
    """Handles logic to get the question bank"""

    def __init__(self, storage: QuestionBankStorageInterface):
        self.storage = storage

    def get_question_bank(self, bank_id: str) -> QuestionBankDTO:
        """
        Retrieve a question bank by its ID.

        Args:
            bank_id: Unique identifier of the question bank.

        Returns:
            QuestionBankDTO: Complete bank details.
        """
        self.check_bank_exists(bank_id, self.storage)

        return self.storage.get_question_bank(bank_id)
