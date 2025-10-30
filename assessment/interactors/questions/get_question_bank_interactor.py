from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface

class GetQuestionBankInteractor(ValidationMixIns):

    def __init__(self,storage: QuestionStorageInterface):
        self.storage=storage

    def get_bank(self,bank_id: str)-> QuestionBankDTO:
        self.check_bank_exists(bank_id,self.storage)
        return self.storage.get_question_bank(bank_id)

