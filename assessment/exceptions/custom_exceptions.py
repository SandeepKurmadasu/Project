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
    def __init__(self,question_ids:list[str]):
        self.question_ids=question_ids


class DuplicateQuestionIdsFound(Exception):
    def __init__(self,question_ids:list[str]):
        self.question_ids=question_ids


class QuestionBankNotFound(Exception):
    def __init__(self,bank_id: str):
        self.bank_id=bank_id


class DuplicateBankNameFound(Exception):
    def __init__(self, name: str):
        self.name = name


class QuestionAlreadyInBank(Exception):
    def __init__(self,bank_id: str,question_ids: list[str]):
        self.bank_id = bank_id
        self.question_ids=question_ids


class QuestionNotInBank(Exception):
    def __init__(self,bank_id: str, question_ids: list[str]):
        self.bank_id = bank_id
        self.question_ids=question_ids


class InvalidQuestionOrder(Exception):
    def __init__(self,invalid_ids: list[str]):
        self.invalid_ids=invalid_ids


class InvalidAlgorithmError(Exception):
    def __init__(self,algorithm: Algorithm):
        self.algorithm=algorithm


class QuestionTextAlreadyExists(Exception):
    def __init__(self,question_texts: list[str]):
        self.question_texts=question_texts