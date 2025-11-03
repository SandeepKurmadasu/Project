"""Interactor to reorder the questions"""
from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)

class ReorderQuestionsInteractor(ValidationMixIns):
    """Handles logic for reorder the questions"""

    def __init__(self,question_storage: QuestionStorageInterface):
        self.question_storage=question_storage

    def reorder_questions(self,bank_id: str,ordered_question_ids: list[str])->QuestionBankDTO:
        """Re_order questions after validation"""
        self.check_bank_exists(bank_id,self.question_storage)
        self.check_valid_question_order(bank_id,ordered_question_ids,self.question_storage)
        return self.question_storage.reorder_questions_in_bank(
            bank_id=bank_id,
            ordered_question_ids=ordered_question_ids
        )
