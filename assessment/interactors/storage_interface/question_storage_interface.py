from abc import ABC, abstractmethod
from typing import Any

from assessment.interactors.dtos import (QuestionDTO, CreateQuestionDTO, \
    UpdateQuestionDTO, SelectionConfigDTO, \
    EvaluateQuestionDTO, QuestionWithEvaluationDTO, ScoringConfigDTO)


class QuestionStorageInterface(ABC):


    @abstractmethod
    def create_questions(self,questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        pass

    @abstractmethod
    def get_questions(self,question_ids: list[str])-> list[QuestionDTO]:
        pass

    @abstractmethod
    def get_texts(self,question_texts: list[str]) -> list[QuestionDTO]:
        pass

    @abstractmethod
    def update_questions(self,questions: list[UpdateQuestionDTO]) -> list[QuestionDTO]:
        pass

    @abstractmethod
    def get_next_n_questions(self,config: SelectionConfigDTO)-> list[QuestionDTO]:
        pass

    @abstractmethod
    def evaluate_question(self,question: QuestionDTO, answer: Any) -> EvaluateQuestionDTO:
        pass

    @abstractmethod
    def get_score_for_question(self,current_question: QuestionWithEvaluationDTO,
                               already_attempted: list[QuestionWithEvaluationDTO],
                               config: ScoringConfigDTO) -> int:
        pass
