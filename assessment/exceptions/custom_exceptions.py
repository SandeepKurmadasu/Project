from assessment.interactors.dtos import Algorithm


class DuplicateQuestionTextFound(Exception):
    def __init__(self, question_texts: list[str]):
        self.question_texts = question_texts


class UnexpectedQuestionTypeFound(Exception):
    def __init__(self, question_types: list[str]):
        self.question_types = question_types


class UnexpectedDifficultyFound(Exception):
    def __init__(self, difficulties: list[str]):
        self.difficulties = difficulties


class QuestionNotFound(Exception):
    def __init__(self, question_ids: list[str]):
        self.question_ids = question_ids


class DuplicateQuestionIdsFound(Exception):
    def __init__(self, question_ids: list[str]):
        self.question_ids = question_ids


class QuestionBankNotFound(Exception):
    def __init__(self, bank_id: str):
        self.bank_id = bank_id


class DuplicateBankNameFound(Exception):
    def __init__(self, name: str):
        self.name = name


class QuestionAlreadyInBank(Exception):
    def __init__(self, bank_id: str, question_ids: list[str]):
        self.bank_id = bank_id
        self.question_ids = question_ids


class QuestionNotInBank(Exception):
    def __init__(self, bank_id: str, question_ids: list[str]):
        self.bank_id = bank_id
        self.question_ids = question_ids


class InvalidQuestionOrder(Exception):
    def __init__(self, invalid_ids: list[str]):
        self.invalid_ids = invalid_ids


class InvalidAlgorithmError(Exception):
    def __init__(self, algorithm: Algorithm):
        self.algorithm = algorithm


class AssessmentIdNotFound(Exception):
    def __init__(self, assessment_id: str):
        self.assessment_id = assessment_id


class AttemptIdNotFound(Exception):
    def __init__(self, attempt_id: str):
        self.attempt_id = attempt_id


class DuplicateQuestionsFound(Exception):
    def __init__(self, question_ids: list[str]):
        self.question_ids = question_ids


class InvalidAssessmentTypesFound(Exception):
    def __init__(self, assessment_types: list[str]):
        self.assessment_types = assessment_types


class PassingMarksExceedTotalError(Exception):
    def __init__(self, passing_marks: int, total_marks: int):
        self.passing_marks = passing_marks
        self.total_marks = total_marks
        super().__init__(
            f"Passing marks ({passing_marks}) cannot be greater than total marks ({total_marks})."
        )


class AssessmentInvalidPassPercentage(Exception):
    def __init__(self, percentages: list[int]):
        self.percentages = percentages

class AlreadyAttemptedExist(Exception):
    def __init__(self,question_id: str):
        self.question_id = question_id