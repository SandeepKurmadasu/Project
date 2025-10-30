from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class RemoveQuestionFromBankInteractor(ValidationMixIns):

    def __init__(self,question_storage: QuestionStorageInterface):
        self.question_storage=question_storage

    def remove_question_from_bank(self,bank_id: str,question_ids: list[str])->QuestionBankDTO:
        self.check_bank_exists(bank_id,self.question_storage)
        self.check_questions_exist(question_ids,self.question_storage)
        self.check_questions_in_bank(bank_id,question_ids,self.question_storage)
        return self.question_storage.remove_question_from_bank(bank_id=bank_id,question_ids=question_ids)

