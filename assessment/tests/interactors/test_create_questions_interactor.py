import pytest
from datetime import datetime
from assessment.interactors.questions.create_questions_interactor import CreateQuestionsInteractor
from assessment.interactors.dtos import CreateQuestionDTO, QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionType, Difficulty


@pytest.fixture
def storage():
    # simple autospec to match interface
    from unittest.mock import create_autospec
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return CreateQuestionsInteractor(question_storage=storage)


def test_create_questions_successfully_for_all_types(interactor, storage, snapshot):
    fixed_time = datetime(2025, 11, 1, 10, 0, 0)

    questions = [

        CreateQuestionDTO(
            question_text="What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty=Difficulty.EASY,
            topic_id="T001",
            options=[{"id": "1", "text": "2"}, {"id": "2", "text": "4"}],
            correct_option_ids=["2"]
        ),

        CreateQuestionDTO(
            question_text="Select programming languages.",
            question_type=QuestionType.MCQ_MULTI,
            difficulty=Difficulty.MEDIUM,
            topic_id="T002",
            options=[{"id": "1", "text": "Python"}, {"id": "2", "text": "C++"}, {"id": "3", "text": "HTML"}],
            correct_option_ids=["1", "2"]
        ),
        CreateQuestionDTO(
            question_text="Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty=Difficulty.MEDIUM,
            topic_id="T003",
            correct_boolean=True
        ),
        CreateQuestionDTO(
            question_text="_____ is the capital of France.",
            question_type=QuestionType.FILL_BLANK,
            difficulty=Difficulty.EASY,
            topic_id="T004",
            correct_fill_text="Paris"
        ),
        CreateQuestionDTO(
            question_text="Match the countries with capitals.",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty=Difficulty.HARD,
            topic_id="T005",
            correct_pairs=[
                {"left": "France", "right": "Paris"},
                {"left": "Japan", "right": "Tokyo"}
            ]
        ),
    ]

    expected_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
            topic_id="T001",
            correct_answer=["2"],
            created_at=fixed_time,
            updated_at=fixed_time,
            options=["2", "4"]
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Select programming languages.",
            question_type=QuestionType.MCQ_MULTI,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T002",
            correct_answer=["1", "2"],
            created_at=fixed_time,
            updated_at=fixed_time,
            options=["Python", "C++", "HTML"]
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T003",
            correct_answer=True,
            created_at=fixed_time,
            updated_at=fixed_time
        ),
        QuestionDTO(
            question_id="Q004",
            question_text="_____ is the capital of France.",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.EASY,
            topic_id="T004",
            correct_answer="Paris",
            created_at=fixed_time,
            updated_at=fixed_time
        ),
        QuestionDTO(
            question_id="Q005",
            question_text="Match the countries with capitals.",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty_level=Difficulty.HARD,
            topic_id="T005",
            correct_answer=[
                {"left": "France", "right": "Paris"},
                {"left": "Japan", "right": "Tokyo"}
            ],
            created_at=fixed_time,
            updated_at=fixed_time
        ),
    ]

    storage.create_questions.return_value = expected_questions

    # ACT
    result = interactor.create_questions(questions)

    # ASSERT
    storage.create_questions.assert_called_once()
    assert result == expected_questions
    snapshot.assert_match(repr(result), "test_create_questions_successfully_for_all_types")
