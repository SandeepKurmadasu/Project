from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface

class AddQuestionsToBankInteractor(ValidationMixIns):
    def __init__(self,storage: QuestionStorageInterface):
        self.storage=storage

    def add_question(self, bank_id: str, question_ids: list[str]) -> QuestionBankDTO:
        self.check_bank_exists(bank_id, self.storage)
        self.check_questions_exist(question_ids, self.storage)
        self.check_question_not_in_bank(bank_id, question_ids, self.storage)

        return self.storage.add_question_to_bank(
            bank_id=bank_id,
            question_ids=question_ids
        )