"""Interactor to reorder the questions"""
from typing import List

from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import (
    QuestionBankStorageInterface
)

class ReorderQuestionsInteractor(AssessmentValidationMixIn):
    """Handles logic for reordering questions in a bank"""

    def __init__(self, question_bank_storage: QuestionBankStorageInterface):
        self.question_bank_storage = question_bank_storage

    def reorder_questions(self, bank_id: str, ordered_question_ids: List[str]) -> QuestionBankDTO:
        """Reorder questions in the bank after validation"""
        self.check_bank_exists(bank_id, self.question_bank_storage)
        self.check_valid_question_order(bank_id, ordered_question_ids, self.question_bank_storage)

        return self.question_bank_storage.reorder_questions_in_bank(
            bank_id=bank_id,
            ordered_question_ids=ordered_question_ids
        )
