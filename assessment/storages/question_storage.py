from typing import Any

from assessment.interactors.dtos import CreateQuestionDTO, QuestionDTO, UpdateQuestionDTO, SelectionConfigDTO, \
    EvaluateQuestionDTO, QuestionWithEvaluationDTO, ScoringConfigDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO


class QuestionStorage(QuestionStorageInterface):

    def create_questions(self,questions: list[CreateQuestionDTO]) ->list[QuestionDTO]:
        pass

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        pass

    def create_question_bank(self,name: str) -> QuestionBankDTO:
        pass

    def get_question_bank(self,bank_id: str) -> QuestionBankDTO:
        pass

    def add_question_to_bank(self,bank_id: str,question_ids: list[str]) -> QuestionBankDTO:
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