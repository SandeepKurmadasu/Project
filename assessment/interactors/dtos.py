import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


class QuestionType(enum.Enum):
    MCQ_SINGLE = "MCQ_SINGLE"
    MCQ_MULTI = "MCQ_MULTI"
    TRUE_FALSE = "TRUE_FALSE"
    FILL_BLANK = "FILL_BLANK"
    MATCH_PAIRS = "MATCH_PAIRS"


class Difficulty(enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


@dataclass
class CreateQuestionDTO:
    question_text: str
    question_type: QuestionType
    difficulty: Difficulty
    topic_id: str  # TODO Check once for this
    options: Optional[List[dict[str,str]]]
    correct_option_ids: Optional[List[str]]
    correct_boolean: Optional[bool] = None
    correct_fill_text: Optional[str] = None
    left_items: Optional[List[str]] = None
    right_items: Optional[List[str]] = None
    correct_pairs: Optional[List[List[int]]] = None

@dataclass
class QuestionDTO:
    question_id: str
    question_text: str
    question_type: QuestionType
    difficulty_level: Difficulty
    topic_id: str
    correct_answer: Any
    created_at: datetime
    updated_at: datetime
    left_items: Optional[List[str]] = None
    right_items: Optional[List[str]] = None
    options: Optional[list[str]] = None


@dataclass
class UpdateQuestionDTO:
    question_id: str
    question_type: QuestionType
    difficulty: Difficulty
    question_text: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option_ids: Optional[List[str]] = None
    correct_boolean: Optional[bool] = None
    correct_fill_text: Optional[str] = None
    left_items: Optional[List[str]] = None
    right_items: Optional[List[str]] = None
    correct_pairs: Optional[List[List[int]]] = None

@dataclass
class QuestionBankDTO:
    bank_id: str
    name: str
    question_ids: list[str]
    created_at: str
    updated_at: str


@dataclass
class AddToBankDTO:
    bank_id: str
    question_ids: List[str]


@dataclass
class AttemptedQuestionDTO:
    question_id: str
    is_correct: bool


class Algorithm(enum.Enum):
    FIXED = "FIXED"
    RANDOM = "RANDOM"
    DIFFICULTY_MIX = "DIFFICULTY_MIX"


@dataclass
class SelectionConfigDTO:
    question_bank_id: str
    number_of_questions: int
    algorithm: Algorithm
    difficulty_weights: Optional[Dict[Difficulty, int]] = None
    already_attempted_questions: Optional[List[AttemptedQuestionDTO]] = None

@dataclass
class AnswerStatus(enum.Enum):
    CORRECT = "CORRECT"
    PARTIALLY_CORRECT = "PARTIALLY_CORRECT"
    INCORRECT = "INCORRECT"


@dataclass
class EvaluateQuestionDTO:
    is_correct: AnswerStatus
    correct_count: Optional[int] = None
    total_count: Optional[int] = None


@dataclass
class QuestionWithEvaluationDTO:
    question_id: str
    evaluation_result: bool


@dataclass
class ScoringConfigDTO:
    marks_if_correct: int= 2
    marks_if_wrong: int= -1
