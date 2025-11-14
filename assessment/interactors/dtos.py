from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from typing import Optional, List, Dict, Any

from course_management.interactors.dtos import StatusEnum


class QuestionType(Enum):
    MCQ_SINGLE = "MCQ_SINGLE"
    MCQ_MULTI = "MCQ_MULTI"
    TRUE_FALSE = "TRUE_FALSE"
    FILL_BLANK = "FILL_BLANK"
    MATCH_PAIRS = "MATCH_PAIRS"


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


@dataclass
class CreateQuestionDTO:
    question_text: str
    question_type: QuestionType
    difficulty: Difficulty
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
    correct_answer: Any
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


class Algorithm(Enum):
    FIXED = "FIXED"
    RANDOM = "RANDOM"
    DIFFICULTY_MIX = "DIFFICULTY_MIX"


@dataclass
class SelectionConfigDTO:
    question_bank_id: str
    number_of_questions: int
    algorithm: Algorithm
    already_attempted_questions: list[str] = None
    difficulty_weights: Optional[Dict[Difficulty, int]] = None

@dataclass
class AnswerStatus(Enum):
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


class ResponseEnum(Enum):
    CORRECT = "CORRECT"
    WRONG = "WRONG"
    PARTIAL_CORRECT = "PARTIAL_CORRECT"


class AssessmentTypeEnum(Enum):
    QUIZ = "QUIZ"
    MODULE_EXAM = "MODULE_EXAM"
    COURSE_EXAM = "COURSE_EXAM"
    ASSIGNMENT = "ASSIGNMENT"


@dataclass
class AssessmentAttemptDTO:
    attempt_id: str
    user_id: str
    assessment_id: str
    total_points: int
    question_ids: list[str]
    status: StatusEnum
    started_at: datetime


@dataclass
class AssessmentAttemptProgressDTO:
    attempt_id: str
    user_id: str
    assessment_id: str
    total_points: int
    status: StatusEnum


@dataclass
class CreateAssessmentAttemptDTO:
    user_id: str
    assessment_id: str


@dataclass
class DisplayQuestionDTO:
    question_id: str
    question_text: str
    options: list[Dict[str, str]]


@dataclass
class AttemptScoreDTO:
    attempt_id: str
    score: int
    user_id: str


@dataclass
class AssessmentDTO:
    assessment_id: str
    assessment_title: str
    assessment_type: AssessmentTypeEnum
    description: str
    pass_marks: int
    icon: str
    no_of_questions: int
    marks: int
    pass_percentage: int
    easy_count: int | None
    medium_count: int | None
    hard_count: int | None
    attempts_limit: int
    estimate_duration_in_mins: int



@dataclass
class CreateAssessmentDTO:
    assessment_title: str
    assessment_type: AssessmentTypeEnum
    description: str
    icon: str
    no_of_questions: int
    attempts_limit: int
    pass_percentage: int
    easy_count: int | None
    medium_count: int | None
    hard_count: int | None
    estimate_duration_in_mins: int



@dataclass
class SubmitResponseDTO:
    assessment_id: str
    attempt_id: str
    question_id: str
    response: str


@dataclass
class ScoreConfigDTO:
    points = {
        Difficulty.EASY: {ResponseEnum.CORRECT: 2, ResponseEnum.WRONG: -1},
        Difficulty.MEDIUM: {ResponseEnum.CORRECT: 3, ResponseEnum.WRONG: -1},
        Difficulty.HARD: {ResponseEnum.CORRECT: 5, ResponseEnum.WRONG: -2},
    }


@dataclass
class UserQuestionSubmittedDTO:
    attempt_id: str
    question_id: str
    response: str
    is_correct: AnswerStatus


@dataclass
class ScoreResponseDTO:
    question_response: AnswerStatus
    question_difficulty: Difficulty
    correct_options_count: int
    total_option_count: int

