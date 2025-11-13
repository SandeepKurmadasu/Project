from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface


class QuestionBankStorage(QuestionBankStorageInterface):


    def create_question_bank(self, name: str) -> QuestionBankDTO:
        pass

    def get_question_bank(self,bank_id: str) -> QuestionBankDTO:
        pass

    def add_questions_to_bank(self,bank_id: str,question_ids: list[str]) -> QuestionBankDTO:
        pass

    def remove_question_from_bank(self,bank_id: str,question_ids: list[str]) ->QuestionBankDTO:
        pass

    def reorder_questions_in_bank(self,bank_id: str,ordered_question_ids: list[str]) ->QuestionBankDTO:
        pass

    def get_question_bank_by_name(self,name: str) -> list[QuestionBankDTO]:
        pass
        #return QuestionBank.objects.filter(name=name).first()

    def add_questions_to_bank_ordered(self,bank_id: str, ordered_ids: list[dict]) -> QuestionBankDTO:
        pass
        # objs=[
        #     QuestionBankQuestion(
        #         bank_id=bank_id,
        #         question_id=item["question_id"],
        #         position=item["position"]
        #     )for item in ordered_ids
        # ]
        # QuestionBankQuestion.objects.bulk_create(objs)
        #
        # return self.get_question_bank(bank_id)

    def create_question_bank_for_assessment(self, name: str, assessment_id: str) -> QuestionBankDTO:
        pass

    def get_assessment_question_bank(self, assessment_id: str) -> QuestionBankDTO:
        pass
