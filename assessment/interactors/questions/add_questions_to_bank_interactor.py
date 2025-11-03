"""Interactor for adding questions to the questionbank."""

from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import (
     QuestionStorageInterface
)


class AddQuestionsToBankInteractor(ValidationMixIns):
    """Handles logic for adding questions to a specific question bank."""
    def __init__(self,storage: QuestionStorageInterface):
        self.storage=storage

    def add_question(self, bank_id: str, question_ids: list[str]) -> QuestionBankDTO:
        """Add Questions to a question bank after validation.

        Args:
            bank_id (str): Unique ID of the question bank.
            question_ids (list[str]): List of question IDs to add.

        Returns:
            QuestionBankDTO: Updated question bank data transfer object.
         """
        self._validate_inputs(bank_id,question_ids)
        return self.storage.add_question_to_bank(bank_id=bank_id,question_ids=question_ids)

    def _validate_inputs(self, bank_id: str, question_ids: list[str]):
        """Validate that bank and questions exist and aren’t already added."""

        self.check_bank_exists(bank_id, self.storage)
        self.check_questions_exist(question_ids, self.storage)
        self.check_question_not_in_bank(bank_id, question_ids, self.storage)
