from assessment.interactors.dtos import QuestionDTO
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.models import QuestionBankQuestion


class QuestionBankQuestionStorage(QuestionBankQuestionStorageInterface):


    def remove_question_from_bank(self, bank_id: str, question_ids: list[str]):
        pass

    def reorder_questions_in_bank(self, bank_id: str, ordered_question_ids: list[str]):
        bank_questions = QuestionBankQuestion.objects.filter(
            question_bank_id=bank_id,
            question_id_in=ordered_question_ids
        )
        question_map = {str(bq.question.question_id): bq for bq in bank_questions}
        updated_questions = []
        for new_order, question_id in enumerate(ordered_question_ids, start=1):
            bank_question = question_map[question_id]
            bank_question.order = new_order
            updated_questions.append(bank_question)

        QuestionBankQuestion.objects.bulk_update(updated_questions, ['order'])

        return updated_questions

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
