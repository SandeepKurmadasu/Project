from abc import ABC, abstractmethod

from assessment.interactors.dtos import QuestionBankQuestionDTO, QuestionDTO


class QuestionBankQuestionStorageInterface(ABC):


    @abstractmethod
    def remove_question_from_bank(self, bank_id: str, question_ids: list[str]) -> QuestionBankQuestionDTO:
        pass

    @abstractmethod
    def reorder_questions_in_bank(self, bank_id: str, ordered_question_ids: list[str]) -> QuestionBankQuestionDTO:
        pass

    @abstractmethod
    def add_questions_to_bank_ordered(self, bank_id: str, ordered_ids: list[dict]) -> QuestionBankQuestionDTO:
        pass

    @abstractmethod
    def get_bank_questions(self, bank_id: str)-> list[QuestionDTO]:
        pass

    @abstractmethod
    def get_existing_question_ids(self, bank_id: str, question_ids: list[str]):
        pass

    @abstractmethod
    def normalize_order(self, bank_id: str):
        pass

