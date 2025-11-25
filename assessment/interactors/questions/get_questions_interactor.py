"""Interactor to get the questions"""
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)

class GetQuestionsInteractor(AssessmentValidationMixIn):
    """Handles the logic for get the questions"""

    def __init__(self,question_storage: QuestionStorageInterface):
        self.question_storage=question_storage

    def get_questions(self, question_ids: list[str]) -> list[QuestionDTO]:
        """get the questions after validation"""
        self.check_if_question_ids_exists_in_db(
            question_ids=question_ids,
            question_storage=self.question_storage
        )



        return self.question_storage.get_questions(question_ids=question_ids)
