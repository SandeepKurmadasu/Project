from typing import Any

from assessment.interactors.dtos import  QuestionDTO, UpdateQuestionDTO, SelectionConfigDTO, \
    EvaluateQuestionDTO, QuestionWithEvaluationDTO, ScoringConfigDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO
from assessment.models import Question


class QuestionStorage(QuestionStorageInterface):

    def create_questions(self,questions: list[Question]) ->list[QuestionDTO]:
        created_questions = Question.objects.bulk_create(questions)


        return [
            QuestionDTO(
                question_id=str(q.id),
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty_level=q.difficulty,
                options=q.options,
                correct_answer=q.correct_option_ids,
                topic_id=q.topic.topic_id,
                created_at=q.created_at,
                updated_at=q.updated_at,
            )
            for q in created_questions
        ]

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        questions=Question.objects.filter(question_id__in=question_ids)
        question_dtos=[
            QuestionDTO(
                question_id=q.id,
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty_level=q.difficulty,
                options=q.options,
                topic_id=q.topic.topic_id,
                correct_answer=q.correct_option_ids,
                created_at=q.created_at,
                updated_at=q.updated_at
            )
            for q in questions
        ]
        return question_dtos

    def get_texts(self,question_texts: list[str]) -> list[QuestionDTO]:
        pass

    def create_question_bank(self,name: str) -> QuestionBankDTO:
        pass

    def get_question_bank(self,bank_id: str) -> QuestionBankDTO:
        pass

    def add_questions_to_bank(self,bank_id: str,question_ids: list[str]) -> QuestionBankDTO:
        pass

    def get_all_question_banks(self) -> list[QuestionBankDTO]:
        pass

    def remove_question_from_bank(self,bank_id: str,question_ids: list[str]) ->QuestionBankDTO:
        pass

    def update_questions(self,questions: list[UpdateQuestionDTO]) ->list[QuestionDTO]:
        pass

    def reorder_questions_in_bank(self,bank_id: str,ordered_question_ids: list[str]) ->QuestionBankDTO:
        pass

    def get_next_n_questions(self,config: SelectionConfigDTO) ->list[QuestionDTO]:
        pass

    def evaluate_question(self,question: QuestionDTO, answer: Any) -> EvaluateQuestionDTO:
        pass

    def get_score_for_question(self,current_question: QuestionWithEvaluationDTO,already_attempted: list[QuestionWithEvaluationDTO],config: ScoringConfigDTO) -> int:
        pass

    def check_questions_in_bank(self,question_ids: list[str]) ->list[QuestionDTO]:
        pass