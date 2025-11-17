from typing import Dict

from django.core.exceptions import ObjectDoesNotExist

from assessment.exceptions.custom_exceptions import DuplicateQuestionTextFound, \
    UnexpectedQuestionTypeFound, \
    UnexpectedDifficultyFound, DuplicateQuestionIdsFound, QuestionNotFound, \
    QuestionBankNotFound, \
    DuplicateBankNameFound, QuestionAlreadyInBank, QuestionNotInBank, \
    InvalidQuestionOrder, InvalidAlgorithmError, \
    AttemptIdNotFound, AssessmentIdNotFound
from assessment.interactors.dtos import QuestionType, Difficulty, Algorithm, CreateQuestionDTO
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import \
    QuestionBankStorageInterface

from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface


class AssessmentValidationMixIn:

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
    def check_duplicate_question_ids(question_ids: list[str]):
        seen = []
        duplicates = []
        for q in question_ids:
            if q in seen and q not in duplicates:
                duplicates.append(q)
            else:
                seen.append(q)

        if duplicates:
            raise DuplicateQuestionIdsFound(question_ids=duplicates)

    @staticmethod
    def check_if_question_ids_exists_in_db(question_ids: list[str],
                                           question_storage: QuestionStorageInterface):
        existing_questions = question_storage.get_questions(
            question_ids=question_ids)
        existing_ids = {q.question_id for q in existing_questions}
        missing_ids = [qid for qid in question_ids if qid not in existing_ids]

        if missing_ids:
            raise QuestionNotFound(question_ids=missing_ids)

    @staticmethod
    def check_bank_exists(bank_id: str,
                          question_bank_storage: QuestionBankStorageInterface):
        try:
            question_bank_storage.get_question_bank(bank_id)
        except ObjectDoesNotExist:
            raise QuestionBankNotFound(bank_id=bank_id)

    @staticmethod
    def check_duplicate_bank_name(name: str,
                                  question_bank_storage: QuestionBankStorageInterface):
        existing_bank = question_bank_storage.get_question_bank_by_name(
            name=name)

        if existing_bank:
            raise DuplicateBankNameFound(name=name)

    @staticmethod
    def _get_question_status(bank_id: str, question_ids: list[str],
                             question_bank_question_storage: QuestionBankQuestionStorageInterface):
        bank = question_bank_question_storage.get_bank_questions(bank_id)
        bank_question_ids = [obj.question_id for obj in bank]
        question_already_in_bank = [qid for qid in question_ids if
                                    qid in bank_question_ids]

        return question_already_in_bank

    def check_questions_not_in_bank(self, bank_id: str,
                                    question_ids: list[str],
                                    question_bank_question_storage: QuestionBankQuestionStorageInterface):
        question_already_in_bank = self._get_question_status(bank_id,
                                                             question_ids,
                                                             question_bank_question_storage)

        if question_already_in_bank:
            raise QuestionAlreadyInBank(question_ids=question_already_in_bank,
                                        bank_id=bank_id)

    @staticmethod
    def check_questions_in_bank(bank_id: str, question_ids: list[str],
                                question_bank_question_storage: QuestionBankQuestionStorageInterface):
        question_already_in_bank = AssessmentValidationMixIn._get_question_status(
            bank_id, question_ids, question_bank_question_storage)

        if not question_already_in_bank:
            raise QuestionNotInBank(question_ids=question_already_in_bank,
                                    bank_id=bank_id)

    def check_valid_question_order(self, bank_id: str,
                                   ordered_question_ids: list[str], storage):

        bank = storage.get_bank_questions(bank_id)
        bank_question_ids = set([obj.question_id for obj in bank])

        missing_ids = [qid for qid in ordered_question_ids if qid not in bank_question_ids]
        if missing_ids:
            raise InvalidQuestionOrder(invalid_ids=missing_ids)

        self.check_duplicate_question_ids(question_ids=ordered_question_ids)

    @staticmethod
    def check_valid_number_of_questions(n: int):
        if n <= 0:
            raise ValueError("number_of_questions must be > 0")

    @staticmethod
    def check_valid_algorithm(algorithm: Algorithm):
        valid_algorithms = [Algorithm.FIXED, Algorithm.RANDOM,
                            Algorithm.DIFFICULTY_MIX]
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

    @staticmethod
    def validate_attempt_exists(attempt_id: str,
                                attempt_storage: AttemptStorageInterface):
        is_attempt = attempt_storage.check_attempt_exist(attempt_id=attempt_id)

        if not is_attempt:
            raise AttemptIdNotFound(attempt_id=attempt_id)

    @staticmethod
    def validate_assessment_exists(assessment_id: str,
                                   assessment_storage: AssessmentStorageInterface):
        is_assessment = assessment_storage.assessment_exists(
            assessment_id=assessment_id)

        if not is_assessment:
            raise AssessmentIdNotFound(assessment_id=assessment_id)

    @staticmethod
    def _check_duplicate_options(values, qtype):
        ids = []
        for option in values:
            ids.append(list(option.keys())[0])
        if len(ids) != len(set(ids)):
            raise ValueError(f"{qtype}: duplicate options not allowed")

    @staticmethod
    def _check_minimum_options(values, qtype):
        if len(values) < 2:
            raise ValueError(f"{qtype}: at least 2 options required")

    @staticmethod
    def _check_answer_in_options(correct_answer, options, qtype):
        valid_ids = {list(opt.keys())[0] for opt in options}

        for ans in correct_answer:
            if ans not in valid_ids:
                raise ValueError(
                    f"{qtype}: correct_answer '{ans}' not found. Valid IDs: {sorted(valid_ids)}"
                )


    def validate_question_payload(self,q: CreateQuestionDTO):
        qtype = q.question_type

        # MCQ SINGLE
        if qtype == QuestionType.MCQ_SINGLE:
            values = q.options

            self._check_duplicate_options(values, "MCQ_SINGLE")
            self._check_minimum_options(values, "MCQ_SINGLE")
            self._check_answer_in_options(q.correct_answer, q.options, "MCQ_SINGLE")

        # MCQ MULTI
        elif qtype == QuestionType.MCQ_MULTI:
            values = list(q.options)

            self._check_duplicate_options(values, "MCQ_MULTI")
            self._check_minimum_options(values, "MCQ_MULTI")

            for ans in q.correct_answer:
                self._check_answer_in_options(ans, q.options, "MCQ_MULTI")

        # TRUE / FALSE
        elif qtype == QuestionType.TRUE_FALSE:
            values = list(q.options)
            self._check_minimum_options(values, "TRUE_FALSE")

        # FILL_IN_THE_BLANK
        elif qtype == QuestionType.FILL_BLANK:
            if not isinstance(q.correct_answer, str):
                raise ValueError("FILL_BLANK: correct_answer must be string")

        # MATCH PAIRS
        elif qtype == QuestionType.MATCH_PAIRS:
            opts=q.options
            if isinstance(opts, list):
                opts = {k: v for d in opts for k, v in d.items()}

            left = opts.get("left_items", [])
            right = opts.get("right_items", [])

            if len(left) != len(right):
                raise ValueError("MATCH_PAIRS: left_items and right_items must be equal length")

        else:
            raise ValueError("Unknown question type")