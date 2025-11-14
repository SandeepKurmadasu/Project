from assessment.interactors.dtos import QuestionDTO
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface


class QuestionBankQuestionStorage(QuestionBankQuestionStorageInterface):


    def remove_question_from_bank(self, bank_id: str, question_ids: list[str]):
        pass

    def reorder_questions_in_bank(self, bank_id: str, ordered_question_ids: list[str]):
        pass

    def add_questions_to_bank_ordered(self, bank_id: str, ordered_ids: list[dict]):
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

    def get_bank_questions(self, bank_id: str)-> list[QuestionDTO]:
        pass
