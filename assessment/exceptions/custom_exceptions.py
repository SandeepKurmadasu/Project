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
































class MCQMissingOptionsFound(Exception):
    def __init__(self, question_ids: list[str]):
        self.question_ids = question_ids

class MCQMissingCorrectIdsFound(Exception):
    def __init__(self, question_ids: list[str]):
        self.question_ids = question_ids

class MCQInvalidOptionIdsFound(Exception):
    def __init__(self, missing_ids: list[str], question_id: str):
        self.missing_ids = missing_ids
        self.question_id = question_id

class MCQSingleInvalidAnswerCountFound(Exception):
    def __init__(self, question_id: str):
        self.question_id = question_id

class TrueFalseMissingAnswerFound(Exception):
    def __init__(self, question_id: str):
        self.question_id = question_id

class FillBlankMissingAnswerFound(Exception):
    def __init__(self, question_id: str):
        self.question_id = question_id

class MatchPairsMissingPairsFound(Exception):
    def __init__(self, question_id: str):
        self.question_id = question_id

class UnexpectedAnswerFieldsFound(Exception):
    def __init__(self, fields: list[str], question_id: str):
        self.fields = fields
        self.question_id = question_id