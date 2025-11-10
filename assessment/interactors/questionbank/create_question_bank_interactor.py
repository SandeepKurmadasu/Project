"""Interactor for creating the Question Bank"""
from assessment.interactors.common_validation_mixin import ValidationMixIn
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)
from assessment.interactors.dtos import QuestionBankDTO


class CreateQuestionBankInteractor(ValidationMixIn):
    """Handles logic for creating the question bank"""
    def __init__(self, question_storage: QuestionStorageInterface): # TODO add the questionBank Storage interface
        self.storage = question_storage

    def create_question_bank(self, name: str) -> QuestionBankDTO:
        """
        Create a new question bank after validation.

        Args:
            name: Name of the question bank.

        Returns:
            QuestionBankDTO: Newly created question bank.
        """
        self.check_duplicate_bank_name(name, self.storage)

        return self.storage.create_question_bank(name=name)
