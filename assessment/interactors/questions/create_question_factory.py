# pylint: disable=too-few-public-methods
"""This module contains factory classes to create different types of Question objects."""
from abc import ABC, abstractmethod

from assessment.interactors.dtos import CreateQuestionDTO, QuestionType
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
            correct_option_ids=question.correct_option_ids,
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
            correct_option_ids=question.correct_option_ids,
        )


class FillInTheBlankQuestionFactory(BaseQuestionFactory):
    """Factory for creating fill_in_the_blank questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            correct_fill_text=question.correct_fill_text,
        )


class TrueOrFalseQuestionFactory(BaseQuestionFactory):
    """Factory for creating true_or_false questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            correct_boolean=question.correct_boolean,
        )


class MatchThePairsQuestionFactory(BaseQuestionFactory):
    """Factory for creating match_the_pairs questions."""

    def create(self, question: CreateQuestionDTO):
        """Creates and returns a Question object."""

        return Question(
            question_text=question.question_text,
            question_type=question.question_type.value,
            difficulty=question.difficulty.value,
            correct_pairs=question.correct_pairs,
        )


class CreateQuestionFactory:
    """Provides factory instances for each question type and supports bulk creation."""

    @staticmethod
    def get_factory(question_type: QuestionType) -> BaseQuestionFactory:
        """Returns the factory instance for the given question type."""
        all_classes = {
            QuestionType.MCQ_SINGLE: MCQSingleQuestionFactory(),
            QuestionType.MCQ_MULTI: MCQMultiChoiceQuestionFactory(),
            QuestionType.TRUE_FALSE: TrueOrFalseQuestionFactory(),
            QuestionType.FILL_BLANK: FillInTheBlankQuestionFactory(),
            QuestionType.MATCH_PAIRS: MatchThePairsQuestionFactory(),
        }

        return all_classes.get(question_type)

    @staticmethod
    def bulk_create_questions(questions: list[CreateQuestionDTO]):
        """Creates and returns multiple Question objects in bulk."""
        question_objects = []
        for q in questions:
            factory = CreateQuestionFactory.get_factory(q.question_type)
            question_obj = factory.create(q)
            question_objects.append(question_obj)

        return question_objects
