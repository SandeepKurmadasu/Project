from typing import Dict

from django.core.exceptions import ObjectDoesNotExist

from assessment.exceptions.custom_exceptions import DuplicateQuestionTextFound, UnexpectedQuestionTypeFound, \
    UnexpectedDifficultyFound, DuplicateQuestionIdsFound, QuestionNotFound, QuestionBankNotFound, \
    DuplicateBankNameFound, QuestionAlreadyInBank, QuestionNotInBank, InvalidQuestionOrder, InvalidAlgorithmError
from assessment.interactors.dtos import CreateQuestionDTO, QuestionType, Difficulty
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class ValidationMixIns:

    @staticmethod
    def check_duplicate_question_texts(questions: list[CreateQuestionDTO]):
        question_texts=[]
        for q in questions:
            if q.question_text:
                question_texts.append(q.question_text.strip())
        seen=set()
        duplicates=[]
        for text in question_texts:
            if text in seen and text not in duplicates:
                duplicates.append(text)
            else:
                seen.add(text)
        if duplicates:
            raise DuplicateQuestionTextFound(question_texts=duplicates)


    @staticmethod
    def check_invalid_question_type(questions: list[CreateQuestionDTO]):
        valid_types = [qt.value for qt in QuestionType]
        invalid_types = [
            getattr(q.question_type, "value", q.question_type)
            for q in questions
            if getattr(q.question_type, "value", q.question_type) not in valid_types
        ]
        if invalid_types:
            raise UnexpectedQuestionTypeFound(question_types=invalid_types)


    @staticmethod
    def check_invalid_difficulty(questions: list[CreateQuestionDTO]):
        valid_difficulties = [d.value for d in Difficulty]
        invalid_difficulties = [
            getattr(q.difficulty, "value", q.difficulty)
            for q in questions
            if getattr(q.difficulty, "value", q.difficulty) not in valid_difficulties
        ]
        if invalid_difficulties:
            raise UnexpectedDifficultyFound(difficulties=invalid_difficulties)

    @staticmethod
    def check_duplicate_question_ids(question_ids:list[str]):
        seen=set()
        duplicates=[]
        for q in question_ids:
            if q in seen and q not in duplicates:
                duplicates.append(q)
            else:
                seen.add(q)
        if duplicates:
            raise DuplicateQuestionIdsFound(question_ids=duplicates)

    @staticmethod
    def check_if_question_ids_exists_in_db(question_ids:list[str],question_storage: QuestionStorageInterface):
        existing_questions=question_storage.get_questions(question_ids)
        existing_ids={q.question_id for q in existing_questions}
        missing_ids=[qid for qid in question_ids if qid not in existing_ids]
        if missing_ids:
            raise QuestionNotFound(question_ids=missing_ids)

    @staticmethod
    def check_bank_exists(bank_id: str,storage:QuestionStorageInterface):
        try:
            storage.get_question_bank(bank_id)
        except ObjectDoesNotExist:
            raise QuestionBankNotFound


    @staticmethod
    def check_duplicate_bank_name(name: str, storage: QuestionStorageInterface):
        banks = storage.get_all_question_banks()
        for bank in banks:
            if bank.name == name:
                raise DuplicateBankNameFound(name=name)

    @staticmethod
    def check_question_not_in_bank(bank_id: str,question_ids: list[str],storage: QuestionStorageInterface):
        bank=storage.get_question_bank(bank_id)
        if question_ids in bank.question_ids:
            raise QuestionAlreadyInBank(question_ids=question_ids)

    @staticmethod
    def check_questions_exist(question_ids: list[str], storage):
        existing = storage.get_questions(question_ids)
        existing_ids = {q.question_id for q in existing}
        missing = [qid for qid in question_ids if qid not in existing_ids]
        if missing:
            raise QuestionNotFound(question_ids=missing)

    @staticmethod
    def check_questions_in_bank(bank_id: str, question_ids: list[str], storage):
        bank = storage.get_question_bank(bank_id)
        not_in_bank = [qid for qid in question_ids if qid not in bank.question_ids]
        if not_in_bank:
            raise QuestionNotInBank(question_ids=not_in_bank)


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
    def check_valid_algorithm(algorithm: str):
        if algorithm not in ["random", "difficulty_mix"]:
            raise InvalidAlgorithmError(algorithm)

    @staticmethod
    def check_valid_difficulty_weights(weights: Dict[str, int]):
        if not weights:
            return
        valid = {"EASY", "MEDIUM", "HARD"}
        for key in weights:
            if key not in valid:
                raise ValueError(f"Invalid difficulty: {key}")
            if weights[key] < 0:
                raise ValueError(f"Weight for {key} must be >= 0")