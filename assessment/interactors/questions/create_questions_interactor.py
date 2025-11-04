"""Interactor for creating the questions"""
from assessment.interactors.common_validation_mixin import ValidationMixIn
from assessment.interactors.dtos import QuestionDTO,CreateQuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)
from assessment.interactors.questions.create_question_factory import QuestionFactory


class CreateQuestionsInteractor(ValidationMixIn):
    """Handles Logic for creating the Questions"""
    def __init__(self,question_storage: QuestionStorageInterface):
        self.question_storage = question_storage

    def create_questions(self,questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        """Create Questions after validation
        Args:
            list[CreateQuestionDTO]
        Returns:
            QuestionDTO
        """
        self.check_duplicate_question_texts(questions=questions)
        self.check_invalid_question_type(questions=questions)
        question_texts=[qtext.question_text for qtext in questions]
        self.check_if_question_texts_exists_in_db(question_texts=question_texts,question_storage=self.question_storage)
        self.check_invalid_difficulty(questions=questions)

        question_objects = QuestionFactory.bulk_create_questions(questions)
        created_questions = self.question_storage.create_questions(question_objects)

        return created_questions
