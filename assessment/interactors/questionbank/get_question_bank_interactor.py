"""Interactor to get the question bank"""
from assessment.interactors.common_validation_mixin import ValidationMixIn
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)

class GetQuestionBankInteractor(ValidationMixIn):
    """Handles the logic to get the question"""

    def __init__(self,storage: QuestionStorageInterface):
        self.storage=storage

    def get_question_bank(self,bank_id: str)-> QuestionBankDTO:
        """get the question bank after validation"""

        self.check_bank_exists(bank_id,self.storage)
        return self.storage.get_question_bank(bank_id)
