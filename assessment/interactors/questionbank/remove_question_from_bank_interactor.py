"""Interactor for removing the question from the bank"""
from typing import List

from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)

class RemoveQuestionFromBankInteractor(AssessmentValidationMixIn):
    """Handles logic for removing questions from a bank"""

    def __init__(self, question_storage: QuestionStorageInterface):
        self.question_storage = question_storage

    def remove_question_from_bank(self, bank_id: str, question_ids: List[str]) -> QuestionBankDTO:
        """Remove question from bank after validation"""
        self._validate_inputs(bank_id, question_ids)

        return self.question_storage.remove_question_from_bank(
            bank_id=bank_id,
            question_ids=question_ids
        )

    def _validate_inputs(self,bank_id: str, question_ids: List[str]) -> None:
        """Validate bank_exists,question_exist,question_in_bank"""
        self.check_bank_exists(bank_id, self.question_storage)
        self.check_if_question_ids_exists_in_db(question_ids, self.question_storage)
        self.check_questions_in_bank(bank_id, question_ids, self.question_storage)
