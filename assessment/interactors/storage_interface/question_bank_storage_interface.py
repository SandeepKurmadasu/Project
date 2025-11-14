from abc import abstractmethod, ABC

from assessment.interactors.dtos import  QuestionBankDTO


class QuestionBankStorageInterface(ABC):


    @abstractmethod
    def get_question_bank(self, bank_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def get_question_bank_by_name(self, name: str) -> list[QuestionBankDTO]:
        pass

    @abstractmethod
    def create_question_bank_for_assessment(self, name: str, assessment_id: str) -> QuestionBankDTO:
        pass

    @abstractmethod
    def get_assessment_question_bank(self, assessment_id: str) -> QuestionBankDTO:
        pass
