import random
from abc import ABC, abstractmethod
from typing import List

from assessment.interactors.dtos import QuestionDTO, SelectionConfigDTO, Difficulty


class QuestionSelectionStrategy(ABC):

    @abstractmethod
    def select(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> list[QuestionDTO]:
        """Base interface for all question-selection algorithms."""


class FixedSelectionStrategy(QuestionSelectionStrategy):

    def select(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> list[QuestionDTO]:

        return questions[:config.number_of_questions]


class RandomSelectionStrategy(QuestionSelectionStrategy):

    def select(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        available = len(questions)
        required = config.number_of_questions

        # If requested more questions than available → return all, shuffled
        if required >= available:
            random.shuffle(questions)
            return questions

        # Normal random sampling
        return random.sample(questions, required)


class DifficultySelectionStrategy(QuestionSelectionStrategy):

    def select(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        easy = [q for q in questions if q.difficulty_level == Difficulty.EASY]
        medium = [question for question in questions if question.difficulty_level == Difficulty.MEDIUM]
        hard = [question for question in questions if question.difficulty_level == Difficulty.HARD]

        random.shuffle(easy)
        random.shuffle(medium)
        random.shuffle(hard)

        weights = config.difficulty_weights or {}
        easy_count = weights.get(Difficulty.EASY, 0)
        medium_count = weights.get(Difficulty.MEDIUM, 0)
        hard_count = weights.get(Difficulty.HARD, 0)

        result = []
        result.extend(easy[:easy_count])
        result.extend(medium[:medium_count])
        result.extend(hard[:hard_count])

        return result[:config.number_of_questions]
