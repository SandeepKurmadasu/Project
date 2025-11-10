"""Interactor to update the questions"""
from assessment.interactors.common_validation_mixin import ValidationMixIn
from assessment.interactors.dtos import UpdateQuestionDTO, QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)


class UpdateQuestionInteractor(ValidationMixIn):
    """Handles logic to update the questions"""

    def __init__(self, question_storage: QuestionStorageInterface):
        self.question_storage = question_storage

    def update_questions(self, questions: list[UpdateQuestionDTO]) -> list[QuestionDTO]:
        """Update questions after validations"""
        question_ids = [obj.question_id for obj in questions]
        question_texts = [qtext.question_text for qtext in questions]
        question_types = [question.question_type.value for question in questions]
        question_difficulty=[question.difficulty.value for question in questions]


        self.check_duplicate_question_ids(question_ids=question_ids)
        self.check_duplicate_question_texts(question_texts=question_texts)
        self.check_if_question_ids_exists_in_db(
            question_ids=question_ids,
            question_storage=self.question_storage
        )
        self.check_invalid_difficulty(question_difficulty=question_difficulty)
        self.check_invalid_question_type(question_types=question_types)
        self.check_if_question_texts_exists_in_db(question_texts=question_texts,
                                                  question_storage=self.question_storage
        )

        return self.question_storage.update_questions(questions=questions)
