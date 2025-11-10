"""Interactor for creating the questions."""
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import QuestionDTO, CreateQuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface,
)


class CreateQuestionsInteractor(AssessmentValidationMixIn):
    """Handles logic for creating the questions."""

    def __init__(self, question_storage: QuestionStorageInterface):
        self.question_storage = question_storage

    def create_questions(self, questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        """
        Create Questions after validation
        Args:
            questions (list[CreateQuestionDTO]): The list of question data to create.

        Returns:
            QuestionDTO The created question objects.
        """
        question_texts = [question.question_text for question in questions]
        question_types = [question.question_type.value for question in questions]
        question_difficulty=[question.difficulty.value for question in questions]

        self.check_duplicate_question_texts(question_texts=question_texts)
        self.check_invalid_question_type(question_types=question_types)
        self.check_if_question_texts_exists_in_db(
            question_texts=question_texts,
            question_storage=self.question_storage
        )
        self.check_invalid_difficulty(question_difficulty=question_difficulty)

        created_questions = self.question_storage.create_questions(questions)

        return created_questions
