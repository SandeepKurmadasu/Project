from typing import List
import random
from assessment.interactors.common_validation_mixin import ValidationMixIn
from assessment.interactors.dtos import SelectionConfigDTO, QuestionDTO, Difficulty
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface

class GetNextNQuestionsInteractor(ValidationMixIn):
    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage

    def get_questions(self, config: SelectionConfigDTO) -> List[QuestionDTO]:
        self.check_bank_exists(config.question_bank_id, self.storage)
        self.check_valid_number_of_questions(config.number_of_questions)
        self.check_valid_algorithm(config.algorithm)
        self.check_valid_difficulty_weights(config.difficulty_weights or {})

        if config.already_attempted:
            attempted_ids = [a.question_id for a in config.already_attempted]
            self.check_questions_exist(attempted_ids, self.storage)

        bank = self.storage.get_question_bank(config.question_bank_id)
        questions = self.storage.get_questions(bank.question_ids)

        if config.algorithm == "random":
            return self._random_selection(questions, config)
        else:
            return self._difficulty_mix_selection(questions, config)

    @staticmethod
    def _remove_already_done(questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        if not config.already_attempted:
            return questions

        done_ids = []
        for item in config.already_attempted:
            done_ids.append(item.question_id)

        new_list = []
        for q in questions:
            if q.question_id not in done_ids:
                new_list.append(q)
        return new_list

    def _random_selection(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        questions = self._remove_already_done(questions, config)
        random.shuffle(questions)
        return questions[:config.number_of_questions]

    def _difficulty_mix_selection(self, questions: List[QuestionDTO], config: SelectionConfigDTO) -> List[QuestionDTO]:
        questions = self._remove_already_done(questions, config)

        easy = []
        medium = []
        hard = []

        for q in questions:
            if q.difficulty_level == Difficulty.EASY:
                easy.append(q)
            elif q.difficulty_level == Difficulty.MEDIUM:
                medium.append(q)
            else:
                hard.append(q)

        weights = config.difficulty_weights or {}
        easy_count = weights.get("EASY", 0)
        medium_count = weights.get("MEDIUM", 0)
        hard_count = weights.get("HARD", 0)

        result = []
        result.extend(easy[:easy_count])
        result.extend(medium[:medium_count])
        result.extend(hard[:hard_count])

        return result[:config.number_of_questions]