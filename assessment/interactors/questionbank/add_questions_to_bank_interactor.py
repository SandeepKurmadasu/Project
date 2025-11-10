"""Interactor for adding questions to the question bank."""
from typing import List

from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import (
     QuestionStorageInterface
)


class AddQuestionsToBankInteractor(AssessmentValidationMixIn):
    """Handles logic for adding questions to a specific question bank."""

    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage # TODO add the specific storage interface

    def add_questions_to_bank(self, bank_id: str, question_ids: List[str]) -> QuestionBankDTO:
        """
        Add Questions to a question bank after validation.

        Args:
            bank_id: Unique ID of the question bank.
            question_ids: List of question IDs to add.

        Returns:
            QuestionBankDTO: Updated question bank data transfer object.
        """
        self._validate_inputs(bank_id, question_ids)

        ordered_questions=[
            {"question_id": qid, "position": idx + 1}
            for idx, qid in enumerate(question_ids)
        ]

        return self.storage.add_questions_to_bank_ordered(bank_id=bank_id, ordered_ids=ordered_questions)

    def _validate_inputs(self, bank_id: str, question_ids: List[str]) -> None:
        """Validate that bank and questions exist and aren’t already added."""

        self.check_duplicate_question_ids(question_ids)
        self.check_bank_exists(bank_id, self.storage)
        self.check_if_question_ids_exists_in_db(question_ids, self.storage)
        self.check_questions_not_in_bank(bank_id, question_ids, self.storage)
