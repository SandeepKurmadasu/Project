# pylint: disable=too-few-public-methods
"""Strategy pattern implementation for evaluating various question types."""
from abc import ABC, abstractmethod
from typing import Any

from assessment.interactors.dtos import EvaluateQuestionDTO, QuestionType, AnswerStatus


class QuestionEvaluationStrategy(ABC):
    """Abstract base class for evaluating question types."""

    @abstractmethod
    def evaluate(self, user_answer: Any, correct_answer: Any)-> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""


class MCQSingleQuestionStrategy(QuestionEvaluationStrategy):
    """for mcq-single"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        is_correct = str(user_answer).strip().upper() == str(correct_answer).strip().upper()
        status = AnswerStatus.CORRECT if is_correct else AnswerStatus.INCORRECT

        return EvaluateQuestionDTO(
            is_correct = status,
            correct_count=None,
            total_count=None,
        )


class MultiChoiceMCQQuestionStrategy(QuestionEvaluationStrategy):
    """for mcq-multi"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        user_set = {opt.strip().upper() for opt in str(user_answer or "").split(",") if opt.strip()}
        correct_set = {opt.strip().upper() for opt in str(correct_answer or "").split(",") if opt.strip()}
        correct_count = len(user_set & correct_set)
        total_count = len(correct_set)
        wrong_count = len(user_set-correct_set)

        if correct_count == 0 or wrong_count > 0:
            status = AnswerStatus.INCORRECT
        elif correct_count == total_count:
            status = AnswerStatus.CORRECT
        else:
            status = AnswerStatus.PARTIALLY_CORRECT

        return EvaluateQuestionDTO(
            is_correct = status,
            correct_count=correct_count,
            total_count=total_count,
        )


class FillInTheBlankQuestionStrategy(QuestionEvaluationStrategy):
    """for fill-in-the-blank"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        status = AnswerStatus.CORRECT if is_correct else AnswerStatus.INCORRECT

        return EvaluateQuestionDTO(
            is_correct = status,
            correct_count=None,
            total_count=None,
        )


class TrueOrFalseQuestionStrategy(QuestionEvaluationStrategy):
    """for true-or-false"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        status = AnswerStatus.CORRECT if is_correct else AnswerStatus.INCORRECT

        return EvaluateQuestionDTO(
            is_correct = status,
            correct_count=None,
            total_count=None,
        )


class MatchThePairsQuestionStrategy(QuestionEvaluationStrategy):
    """for match-the-pairs"""

    def evaluate(self, user_answer, correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        correct_pairs = set(map(tuple, correct_answer))
        user_pairs = set(map(tuple, user_answer))

        correct_count = len(user_pairs & correct_pairs)
        total_count = len(correct_pairs)

        if correct_count == 0:
            status = AnswerStatus.INCORRECT
        elif correct_count == total_count:
            status = AnswerStatus.CORRECT
        else:
            status = AnswerStatus.PARTIALLY_CORRECT

        return EvaluateQuestionDTO(
            is_correct = status,
            correct_count=correct_count,
            total_count=total_count,
        )


class QuestionStrategy:
    """Factory for retrieving the correct evaluation strategy."""

    @staticmethod
    def get_strategy(question_type: QuestionType) -> QuestionEvaluationStrategy:
        """Returns the strategy instance for the question type."""
        all_classes={
            QuestionType.MCQ_SINGLE: MCQSingleQuestionStrategy(),
            QuestionType.MCQ_MULTI: MultiChoiceMCQQuestionStrategy(),
            QuestionType.FILL_BLANK: FillInTheBlankQuestionStrategy(),
            QuestionType.TRUE_FALSE: TrueOrFalseQuestionStrategy(),
            QuestionType.MATCH_PAIRS: MatchThePairsQuestionStrategy()
        }
        return all_classes.get(question_type)
