from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO

class CreateQuestionBankInteractor(ValidationMixIns):

    def __init__(self,storage: QuestionStorageInterface):
        self.storage=storage

    def create_question_bank(self,name: str)-> QuestionBankDTO:
        self.check_duplicate_bank_name(name, self.storage)
        return self.storage.create_question_bank(name=name)
