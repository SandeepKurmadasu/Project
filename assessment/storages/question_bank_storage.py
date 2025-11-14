from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface


class QuestionBankStorage(QuestionBankStorageInterface):


    def get_question_bank(self,bank_id: str) -> QuestionBankDTO:
        pass

    def get_question_bank_by_name(self,name: str) -> list[QuestionBankDTO]:
        pass
        #return QuestionBank.objects.filter(name=name).first()

    def create_question_bank_for_assessment(self, name: str, assessment_id: str) -> QuestionBankDTO:
        pass

    def get_assessment_question_bank(self, assessment_id: str) -> QuestionBankDTO:
        pass
