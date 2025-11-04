# pylint: disable=too-few-public-methods
"""Strategy pattern implementation for evaluating various question types."""
from abc import ABC, abstractmethod
from assessment.interactors.dtos import EvaluateQuestionDTO, QuestionType


class QuestionEvaluationStrategy(ABC):
    """Abstract base class for evaluating question types."""

    @abstractmethod
    def evaluate(self, user_answer, correct_answer)-> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        raise NotImplementedError


class MCQSingleQuestionStrategy(QuestionEvaluationStrategy):
    """for mcq-single"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        is_correct = str(user_answer).strip() == str(correct_answer).strip()
        return EvaluateQuestionDTO(is_correct = is_correct)


class MultiChoiceMCQQuestionStrategy(QuestionEvaluationStrategy):
    """for mcq-multi"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        user_set = set(map(str.strip, str(user_answer).split(",")))\
            if user_answer else set()
        correct_set = set(map(str.strip, str(correct_answer).split(","))) \
            if correct_answer else set()
        is_correct = user_set == correct_set

        return EvaluateQuestionDTO(is_correct = is_correct)


class FillInTheBlankQuestionStrategy(QuestionEvaluationStrategy):
    """for fill-in-the-blank"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        return EvaluateQuestionDTO(is_correct = is_correct)


class TrueOrFalseQuestionStrategy(QuestionEvaluationStrategy):
    """for true-or-false"""

    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        return EvaluateQuestionDTO(is_correct = is_correct)


class MatchThePairsQuestionStrategy(QuestionEvaluationStrategy):
    """for match-the-pairs"""

    def evaluate(self, user_answer, correct_answer) -> EvaluateQuestionDTO:
        """evaluate and returns the evaluation result"""
        is_correct = user_answer == correct_answer
        return EvaluateQuestionDTO(is_correct = is_correct)


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
