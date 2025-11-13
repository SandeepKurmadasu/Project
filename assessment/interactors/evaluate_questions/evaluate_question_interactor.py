# pylint: disable=too-few-public-methods
"""Interactor for evaluating user answers to questions."""
from typing import Any

from assessment.interactors.dtos import EvaluateQuestionDTO
from assessment.interactors.evaluate_questions.evaluate_strategy_pattern import QuestionStrategy
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface
)


class EvaluateQuestionInteractor:
    """Handles the logic for evaluating a user's answer for a given question."""

    def __init__(self, storage: QuestionStorageInterface):
        """Initialize with a storage interface for accessing question data."""
        self.storage = storage

    def evaluate(self, question_id: str, user_answer: Any) -> EvaluateQuestionDTO:
        """user answer can be str, list, dict - depends on the question type

        Evaluate a user's answer against the correct answer for a given question.

            Args:
                question_id (str): The unique identifier of the question.
                user_answer (str): The user's submitted answer.

            Returns:
                EvaluateQuestionDTO: The evaluation result including correctness and feedback.

        """
        question_list = self.storage.get_questions([question_id])
        question=question_list[0]
        strategy = QuestionStrategy.get_strategy(question.question_type)
        return strategy.evaluate(user_answer, question.correct_answer)
