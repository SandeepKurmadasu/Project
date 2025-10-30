from abc import ABC, abstractmethod
from typing import Any

from assessment.interactors.dtos import QuestionDTO, CreateQuestionDTO, UpdateQuestionDTO, SelectionConfigDTO, \
    EvaluateQuestionDTO
from assessment.interactors.dtos import QuestionBankDTO


class QuestionStorageInterface(ABC):

    @abstractmethod
    def create_questions(self,questions: list[CreateQuestionDTO]) ->list[QuestionDTO]:
        pass

    @abstractmethod
    def get_questions(self,question_ids:list[str])->list[QuestionDTO]:
        pass

    @abstractmethod
    def update_questions(self,questions: list[UpdateQuestionDTO]) ->list[QuestionDTO]:
        pass

    @abstractmethod
    def get_question_bank(self,bank_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def create_question_bank(self,name: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def get_all_question_banks(self) -> list[QuestionBankDTO]:
        pass

    @abstractmethod
    def add_question_to_bank(self,bank_id: str,question_ids: list[str])->QuestionBankDTO:
        pass

    @abstractmethod
    def remove_question_from_bank(self,bank_id: str,question_ids: list[str])->QuestionBankDTO:
        pass

    @abstractmethod
    def reorder_questions_in_bank(self,bank_id: str,ordered_question_ids: list[str])->QuestionBankDTO:
        pass

    @staticmethod
    def get_next_n_questions(self,config: SelectionConfigDTO)->list[QuestionDTO]:
        pass

    @staticmethod
    def evaluate_question(self,question: QuestionDTO, answer: Any) -> EvaluateQuestionDTO:
        pass
