from abc import ABC, abstractmethod

from assessment.interactors.dtos import (QuestionDTO, CreateQuestionDTO, \
    UpdateQuestionDTO)

class QuestionStorageInterface(ABC):


    @abstractmethod
    def create_questions(self,questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        pass

    @abstractmethod
    def get_questions(self,question_ids: list[str])-> list[QuestionDTO]:
        pass

    @abstractmethod
    def update_questions(self,questions: list[UpdateQuestionDTO]) -> list[QuestionDTO]:
        pass
