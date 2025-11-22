# pylint: disable=too-few-public-methods
"""Strategy pattern implementation for evaluating various question types."""
from abc import ABC, abstractmethod
from typing import Any

from assessment.interactors.dtos import EvaluateQuestionDTO, QuestionTypeDTO, AnswerStatus


class QuestionEvaluationStrategy(ABC):
    """Abstract base class for evaluating question types."""

    @abstractmethod
    def evaluate(self, user_answer: Any, correct_answer: Any)-> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""


class MCQSingleQuestionStrategy(QuestionEvaluationStrategy):
    """for mcq-single"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        if isinstance(user_answer, list):
            if len(user_answer) == 1:
                user_answer = user_answer[0]
            else:
                return EvaluateQuestionDTO(
                    is_correct=AnswerStatus.INCORRECT,
                    correct_count=None,
                    total_count=None
                )

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

        user_set = {opt.strip().upper() for opt in user_answer}
        correct_set = {opt.strip().upper() for opt in correct_answer}
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
        user_pairs = set(map(tuple, user_answer))
        correct_pairs = set(map(tuple, correct_answer))

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
    def get_strategy(question_type: QuestionTypeDTO) -> QuestionEvaluationStrategy:
        """Returns the strategy instance for the question type."""
        all_classes={
            QuestionTypeDTO.MCQ_SINGLE: MCQSingleQuestionStrategy(),
            QuestionTypeDTO.MCQ_MULTI: MultiChoiceMCQQuestionStrategy(),
            QuestionTypeDTO.FILL_BLANK: FillInTheBlankQuestionStrategy(),
            QuestionTypeDTO.TRUE_FALSE: TrueOrFalseQuestionStrategy(),
            QuestionTypeDTO.MATCH_PAIRS: MatchThePairsQuestionStrategy()
        }
        return all_classes.get(question_type)
