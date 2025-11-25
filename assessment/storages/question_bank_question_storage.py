from assessment.interactors.dtos import QuestionDTO, OrderedQuestionDTO, QuestionBankQuestionDTO
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.models import QuestionBankQuestion


class QuestionBankQuestionStorage(QuestionBankQuestionStorageInterface):

    def remove_question_from_bank(self, bank_id: str, question_ids: list[str]) -> QuestionBankQuestionDTO:
        """Remove questions from bank and return removed question details"""

        questions_to_remove = QuestionBankQuestion.objects.filter(
            question_bank_id=bank_id,
            question__question_id__in=question_ids
        ).select_related('question')

        questions = [
            OrderedQuestionDTO(
                question_id=str(obj.question.question_id),
                order=obj.order
            )
            for obj in questions_to_remove
        ]

        QuestionBankQuestion.objects.filter(
            question_bank_id=bank_id,
            question_id__in=question_ids
        ).delete()


        self.normalize_order(bank_id)

        return QuestionBankQuestionDTO(
            bank_id=bank_id,
            questions=questions
        )



    def reorder_questions_in_bank(self, bank_id: str, ordered_question_ids: list[str]):
        qs = (
            QuestionBankQuestion.objects
            .filter(question_bank_id=bank_id)
            .select_related("question")
            .order_by("order")
        )

        id_map = {str(obj.question.question_id): obj for obj in qs}

        old_ids = [str(obj.question.question_id) for obj in qs]
        new_ids = []

        for qid in ordered_question_ids:
            if qid in id_map:
                new_ids.append(qid)

        for qid in old_ids:
            if qid not in new_ids:
                new_ids.append(qid)

        for i, qid in enumerate(new_ids, start=1):
            id_map[qid].order = 1000 + i

        QuestionBankQuestion.objects.bulk_update(id_map.values(), ["order"])

        for i, qid in enumerate(new_ids, start=1):
            id_map[qid].order = i

        QuestionBankQuestion.objects.bulk_update(id_map.values(), ["order"])

        return QuestionBankQuestionDTO(
            bank_id=bank_id,
            questions=[
                OrderedQuestionDTO(
                    question_id=id_map[qid].question.question_id,
                    order=id_map[qid].order
                )
                for qid in new_ids
            ]
        )

    def add_questions_to_bank_ordered(self, bank_id: str, ordered_ids: list[dict]):
        objs = [
            QuestionBankQuestion(
                question_bank_id=bank_id,
                question_id=item["question_id"],
                order=item["order"]
            )
            for item in ordered_ids
        ]

        created_questions = QuestionBankQuestion.objects.bulk_create(objs)

        questions = [
            OrderedQuestionDTO(
                question_id=obj.question.question_id,
                order=obj.order
            )
            for obj in created_questions
        ]

        return QuestionBankQuestionDTO(
            bank_id=bank_id,
            questions=questions
        )

    def get_bank_questions(self, bank_id: str) -> list[QuestionDTO]:
        items = QuestionBankQuestion.objects.filter(
            question_bank_id=bank_id
        ).select_related("question")

        return [
            QuestionDTO(
                question_id=item.question.question_id,
                question_text=item.question.question_text,
                question_type=item.question.question_type,
                difficulty_level=item.question.difficulty,
                options=item.question.options,
                correct_answer=item.question.correct_answer,
            )
            for item in items
        ]

    def get_existing_question_ids(self, bank_id: str, question_ids: list[str]):

        return list(
            QuestionBankQuestion.objects.filter(
                question_bank_id=bank_id,
                question_id__in=question_ids
            ).values_list("question_id", flat=True)
        )

    def normalize_order(self, bank_id: str):
        qs = (
            QuestionBankQuestion.objects
            .filter(question_bank_id=bank_id)
            .order_by("order")
        )

        for index, obj in enumerate(qs, start=1):
            obj.order = index

        QuestionBankQuestion.objects.bulk_update(qs, ["order"])
