from typing import List

from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import SelectionConfigDTO, QuestionDTO, Algorithm
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.question_selection.question_selection_strategy import (
FixedSelectionStrategy,
RandomSelectionStrategy,
DifficultySelectionStrategy
)
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class GetNextNQuestionsInteractor(AssessmentValidationMixIn):


    def __init__(self, question_storage: QuestionStorageInterface, question_bank_storage: QuestionBankStorageInterface, question_bank_question_storage: QuestionBankQuestionStorageInterface):
        self.question_storage = question_storage
        self.question_bank_storage = question_bank_storage
        self.question_bank_question_storage = question_bank_question_storage


    def get_questions(self, config: SelectionConfigDTO) -> List[QuestionDTO]:
        self.check_bank_exists(config.question_bank_id, self.question_bank_storage)
        self.check_valid_number_of_questions(config.number_of_questions)
        self.check_valid_algorithm(config.algorithm)
        self.check_valid_difficulty_weights(config.difficulty_weights or {})

        bank_questions = self.question_bank_question_storage.get_bank_questions(config.question_bank_id)
        bank_question_ids = [obj.question_id for obj in bank_questions]
        unattempted_question_ids = self._remove_already_done(config.already_attempted_questions, bank_question_ids)
        if not unattempted_question_ids:
            unattempted_question_ids = bank_question_ids[:]

        questions = self.question_storage.get_questions(unattempted_question_ids)

        strategy = self._get_strategy(config.algorithm)
        selected_questions = strategy.select(questions, config)

        return selected_questions

    @staticmethod
    def _get_strategy(algorithm: Algorithm):
        strategy_map = {
            Algorithm.FIXED: FixedSelectionStrategy(),
            Algorithm.RANDOM: RandomSelectionStrategy(),
            Algorithm.DIFFICULTY_MIX: DifficultySelectionStrategy()
        }
        return strategy_map[algorithm]

    @staticmethod
    def _remove_already_done(already_attempted_questions: List[str], bank_question_ids: list[str]) -> List[str]:

        # If no attempted questions, just return all
        if not already_attempted_questions:
            return [str(qid) for qid in bank_question_ids]

        attempted_set = {str(qid) for qid in already_attempted_questions}

        unattempted = [str(qid) for qid in bank_question_ids if str(qid) not in attempted_set]
        attempted = [str(qid) for qid in bank_question_ids if str(qid) in attempted_set]

        return unattempted + attempted

