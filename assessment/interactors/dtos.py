import enum
from dataclasses import dataclass
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
    topic_id: str
    options: Optional[List[Dict[str, Any]]] = None  # ONLY FOR THE MCQ
    correct_option_ids: Optional[List[str]] = None  # FOR MCQ SINGLE , MULTI
    correct_boolean: Optional[bool] = None  # For TRUE_FALSE
    correct_fill_text: Optional[str] = None  # For FILL_IN_THE_BLANK
    correct_pairs: Optional[List[Dict[str, str]]] = None  # For MATCH_PAIRS


@dataclass
class QuestionDTO:
    question_id: str
    question_text: str
    question_type: str
    difficulty_level: str
    topic_id: str
    options: list[Dict[str]]
    correct_answer: str
    created_at: str
    updated_at: str