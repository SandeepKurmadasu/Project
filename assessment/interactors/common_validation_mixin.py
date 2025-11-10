from typing import Dict

from django.core.exceptions import ObjectDoesNotExist

from assessment.exceptions.custom_exceptions import DuplicateQuestionTextFound, UnexpectedQuestionTypeFound, \
    UnexpectedDifficultyFound, DuplicateQuestionIdsFound, QuestionNotFound, QuestionBankNotFound, \
    DuplicateBankNameFound, QuestionAlreadyInBank, QuestionNotInBank, InvalidQuestionOrder, InvalidAlgorithmError, \
     QuestionTextAlreadyExists
from assessment.interactors.dtos import  QuestionType, Difficulty, Algorithm
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class ValidationMixIn:

    @staticmethod
    def check_duplicate_question_texts(question_texts: list[str]):
        seen = set()
        duplicates = set()

        for text in question_texts:
            if text in seen and text not in duplicates:
                duplicates.add(text)
            else:
                seen.add(text)

        if duplicates:
            raise DuplicateQuestionTextFound(question_texts=list(duplicates))


    @staticmethod
    def check_invalid_question_type(question_types: list[str]):

        valid_types = [qt.value for qt in QuestionType]
        invalid_types = [q
            for q in question_types
            if q not in valid_types
        ]

        if invalid_types:
            raise UnexpectedQuestionTypeFound(question_types=invalid_types)


    @staticmethod
    def check_invalid_difficulty(question_difficulty: list[str]):

        valid_difficulties = [d.value for d in Difficulty]
        invalid_difficulties = [q
            for q in question_difficulty
            if q not in valid_difficulties
        ]

        if invalid_difficulties:
            raise UnexpectedDifficultyFound(difficulties=invalid_difficulties)

    @staticmethod
    def check_duplicate_question_ids(question_ids:list[str]):
        seen = set()
        duplicates = []
        for q in question_ids:
            if q in seen and q not in duplicates:
                duplicates.append(q)
            else:
                seen.add(q)

        if duplicates:
            raise DuplicateQuestionIdsFound(question_ids=duplicates)

    @staticmethod
    def check_if_question_ids_exists_in_db(question_ids: list[str], question_storage: QuestionStorageInterface):
        existing_questions = question_storage.get_questions(question_ids=question_ids)
        existing_ids = {q.question_id for q in existing_questions}
        missing_ids = [qid for qid in question_ids if qid not in existing_ids]

        if missing_ids:
            raise QuestionNotFound(question_ids=missing_ids)

    @staticmethod
    def check_if_question_texts_exists_in_db(question_texts: list[str], question_storage: QuestionStorageInterface):
        existing_texts=question_storage.get_texts(question_texts=question_texts)

        if existing_texts:
            raise QuestionTextAlreadyExists(question_texts=question_texts)

    @staticmethod
    def check_bank_exists(bank_id: str, storage: QuestionStorageInterface):
        try:
            storage.get_question_bank(bank_id)
        except ObjectDoesNotExist:
            raise QuestionBankNotFound(bank_id=bank_id)

    @staticmethod
    def check_duplicate_bank_name(name: str, storage: QuestionStorageInterface):
        existing_bank = storage.get_question_bank_by_name(name=name)

        if existing_bank:
            raise DuplicateBankNameFound(name=name)

    @staticmethod
    def _get_question_status(bank_id: str, question_ids: list[str], storage: QuestionStorageInterface):
        bank = storage.get_question_bank(bank_id)
        question_already_in_bank = [qid for qid in question_ids if qid in bank.question_ids]

        return question_already_in_bank

    def check_questions_not_in_bank(self, bank_id: str, question_ids: list[str], storage: QuestionStorageInterface):
        question_already_in_bank=self._get_question_status(bank_id,question_ids,storage)

        if question_already_in_bank:
            raise QuestionAlreadyInBank(question_ids=question_already_in_bank,bank_id=bank_id)


    @staticmethod
    def check_questions_in_bank(bank_id: str, question_ids: list[str], storage: QuestionStorageInterface):
        question_already_in_bank = ValidationMixIn._get_question_status(bank_id,question_ids,storage)

        if not question_already_in_bank:
            raise QuestionNotInBank(question_ids=question_already_in_bank,bank_id=bank_id)


    def check_valid_question_order(self,bank_id: str, ordered_question_ids: list[str], storage):

        if not ordered_question_ids:
            raise ValueError("ordered_question_ids cannot be empty")

        bank = storage.get_question_bank(bank_id)
        bank_ids = set(bank.question_ids)

        missing_ids = []
        for qid in ordered_question_ids:
            if qid not in bank_ids:
                missing_ids.append(qid)
        if missing_ids:
            raise InvalidQuestionOrder(invalid_ids=missing_ids)

        self.check_duplicate_question_ids(question_ids=ordered_question_ids)

    @staticmethod
    def check_valid_number_of_questions(n: int):
        if n <= 0:
            raise ValueError("number_of_questions must be > 0")

    @staticmethod
    def check_valid_algorithm(algorithm: Algorithm):
        valid_algorithms = [Algorithm.FIXED, Algorithm.RANDOM, Algorithm.DIFFICULTY_MIX]
        if algorithm not in valid_algorithms:
            raise InvalidAlgorithmError(algorithm)

    @staticmethod
    def check_valid_difficulty_weights(weights: Dict[str, int]):
        if not weights:
            return
        valid = {Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD}

        for key in weights:
            if key not in valid:
                raise ValueError(f"Invalid difficulty: {key}")
