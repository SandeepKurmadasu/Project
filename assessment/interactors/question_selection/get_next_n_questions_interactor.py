from typing import List
from assessment.interactors.common_validation_mixin import AssessmentValidationMixIn
from assessment.interactors.dtos import SelectionConfigDTO, QuestionDTO, Algorithm
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.question_selection.question_selection_strategy import (
FixedSelectionStrategy,
RandomSelectionStrategy,
DifficultySelectionStrategy
)
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class GetNextNQuestionsInteractor(AssessmentValidationMixIn):
    def __init__(self, question_storage: QuestionStorageInterface, question_bank_storage: QuestionBankStorageInterface):
        self.question_storage = question_storage
        self.question_bank_storage = question_bank_storage

    def get_questions(self, config: SelectionConfigDTO) -> List[QuestionDTO]: #change the naming
        self.check_bank_exists(config.question_bank_id, self.question_bank_storage)
        self.check_valid_number_of_questions(config.number_of_questions)
        self.check_valid_algorithm(config.algorithm)
        self.check_valid_difficulty_weights(config.difficulty_weights or {})

        bank = self.question_bank_storage.get_question_bank(config.question_bank_id)
        questions = self.question_storage.get_questions(bank.question_ids)

        questions = self._remove_already_done(questions, config)

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
        if algorithm not in strategy_map:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return strategy_map[algorithm]

    @staticmethod
    def _remove_already_done(questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        if not config.already_attempted_questions:
            return questions

        done_ids = {item.question_id for item in config.already_attempted_questions}
        return [q for q in questions if q.question_id not in done_ids]
