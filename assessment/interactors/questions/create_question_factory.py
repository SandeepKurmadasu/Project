# pylint: disable=too-few-public-methods
"""This module contains factory classes to create different types of Question objects."""
from abc import ABC, abstractmethod

from assessment.interactors.dtos import CreateQuestionDTO, QuestionTypeDTO
from assessment.models import Question


class BaseQuestionFactory(ABC):
    """Abstract base class for creating question objects."""

    @abstractmethod
    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""


class MCQSingleQuestionFactory(BaseQuestionFactory):
    """Factory for creating single-choice MCQ questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            options=question.options,
            correct_answer=question.correct_answer,
        )


class MCQMultiChoiceQuestionFactory(BaseQuestionFactory):
    """Factory for creating multi-choice MCQ questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            options=question.options,
            correct_answer=question.correct_answer,
        )


class FillInTheBlankQuestionFactory(BaseQuestionFactory):
    """Factory for creating fill_in_the_blank questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            correct_answer=question.correct_answer,
        )


class TrueOrFalseQuestionFactory(BaseQuestionFactory):
    """Factory for creating true_or_false questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            correct_answer=question.correct_answer,
        )


class MatchThePairsQuestionFactory(BaseQuestionFactory):
    """Factory for creating match_the_pairs questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            options=question.options,
            correct_answer=question.correct_answer,
        )


class CreateQuestionFactory:
    """Provides factory instances for each question type and supports bulk creation."""

    _factories = {
        QuestionTypeDTO.MCQ_SINGLE: MCQSingleQuestionFactory(),
        QuestionTypeDTO.MCQ_MULTI: MCQMultiChoiceQuestionFactory(),
        QuestionTypeDTO.TRUE_FALSE: TrueOrFalseQuestionFactory(),
        QuestionTypeDTO.FILL_BLANK: FillInTheBlankQuestionFactory(),
        QuestionTypeDTO.MATCH_PAIRS: MatchThePairsQuestionFactory(),
    }

    @staticmethod
    def get_factory(question_type: QuestionTypeDTO) -> BaseQuestionFactory:
        """Returns the factory instance for the given question type."""

        return CreateQuestionFactory._factories.get(question_type)

    @staticmethod
    def bulk_create_questions(questions: list[CreateQuestionDTO]):
        """Creates and returns multiple Question objects in bulk."""
        question_objects = []
        for q in questions:
            factory = CreateQuestionFactory.get_factory(q.question_type)
            question_obj = factory.create(q)
            question_objects.append(question_obj)

        return question_objects
