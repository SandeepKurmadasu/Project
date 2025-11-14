from abc import abstractmethod, ABC

from assessment.interactors.dtos import QuestionBankDTO


class QuestionBankStorageInterface(ABC):


    @abstractmethod
    def get_question_bank(self, bank_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def get_question_bank_by_name(self, name: str) -> list[QuestionBankDTO]:
        pass

    @abstractmethod
    def remove_question_from_bank(self, bank_id: str, question_ids: list[str]) -> QuestionBankDTO:
        pass

    @abstractmethod
    def reorder_questions_in_bank(self, bank_id: str, ordered_question_ids: list[str]) -> QuestionBankDTO:
        pass

    @abstractmethod
    def add_questions_to_bank_ordered(self, bank_id: str, ordered_ids: list[dict]) -> QuestionBankDTO:
        pass

    @abstractmethod
    def create_question_bank_for_assessment(self, name: str, assessment_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def get_assessment_question_bank(self, assessment_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def add_questions_to_bank(self,bank_id: str,question_ids: list[str]) -> QuestionBankDTO:
        pass

