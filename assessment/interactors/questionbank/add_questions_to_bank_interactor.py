"""Interactor for adding questions to the question bank."""
from typing import List


from assessment.exceptions.custom_exceptions import QuestionAlreadyInBank
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionBankQuestionDTO
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface

from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class AddQuestionsToBankInteractor(AssessmentValidationMixIn):
    """Handles logic for adding questions to a specific question bank."""

    def __init__(self, question_storage: QuestionStorageInterface, question_bank_storage: QuestionBankStorageInterface, question_bank_question_storage: QuestionBankQuestionStorageInterface):
        self.question_storage = question_storage
        self.question_bank_storage = question_bank_storage
        self.question_bank_question_storage = question_bank_question_storage

    def add_questions_to_bank(self, bank_id: str, question_ids: List[str]) -> QuestionBankQuestionDTO:
        """
        Add Questions to a question bank after validation.

        Args:
            bank_id: Unique ID of the question bank.
            question_ids: List of question IDs to add.

        Returns:
            QuestionBankDTO: Updated question bank data transfer object.
        """
        self._validate_inputs(bank_id, question_ids)

        existing = self.question_bank_question_storage.get_bank_questions(bank_id)
        current_count = len(existing)

        ordered_questions = []
        for idx, qid in enumerate(question_ids):
            ordered_questions.append({
                "question_id": qid,
                "order": current_count + idx + 1
            })

        return self.question_bank_question_storage.add_questions_to_bank_ordered(bank_id=bank_id, ordered_ids=ordered_questions)

    def _validate_inputs(self, bank_id: str, question_ids: List[str]) -> None:
        """Validate that bank and questions exist and aren’t already added."""
        self.check_bank_exists(bank_id, self.question_bank_storage)
        self.check_if_question_ids_exists_in_db(question_ids, self.question_storage)
        self.check_duplicate_question_ids(question_ids)

        existing = self.question_bank_question_storage.get_existing_question_ids(bank_id, question_ids)
        if existing:
            raise QuestionAlreadyInBank(bank_id, existing)

        #self.check_questions_not_in_bank(bank_id, question_ids, self.question_bank_question_storage)
