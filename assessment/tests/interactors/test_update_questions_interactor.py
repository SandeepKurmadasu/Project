import pytest
from datetime import datetime
from unittest.mock import create_autospec

from assessment.interactors.questions.update_questions_interactor import UpdateQuestionInteractor
from assessment.interactors.dtos import UpdateQuestionDTO, QuestionDTO
from assessment.interactors.dtos import Difficulty, QuestionType
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return UpdateQuestionInteractor(question_storage=storage)


def test_update_questions_successfully(interactor, storage, snapshot):
    # ARRANGE
    now = datetime(2025, 11, 1, 10, 0, 0)

    questions_to_update = [
        UpdateQuestionDTO(
            question_id="Q001",
            question_type=QuestionType.MCQ_SINGLE,
            question_text="Updated: What is 2 + 2?",
            difficulty=Difficulty.MEDIUM,
            options=[{"id": "1", "text": "3"}, {"id": "2", "text": "4"}],
            correct_option_ids=["2"]
        ),
        UpdateQuestionDTO(
            question_id="Q002",
            question_type=QuestionType.MCQ_MULTI,
            question_text="Updated: Select even numbers",
            difficulty=Difficulty.HARD,
            options=[{"id": "1", "text": "1"}, {"id": "2", "text": "2"}, {"id": "3", "text": "4"}],
            correct_option_ids=["2", "3"]
        ),
        UpdateQuestionDTO(
            question_id="Q003",
            question_type=QuestionType.TRUE_FALSE,
            question_text="Updated: Python is dynamically typed?",
            difficulty=Difficulty.MEDIUM,
            correct_boolean=True
        ),
        UpdateQuestionDTO(
            question_id="Q004",
            question_type=QuestionType.FILL_BLANK,
            question_text="Updated: Fill the blank - Python is ____ language",
            difficulty=Difficulty.EASY,
            correct_fill_text="interpreted"
        ),
        UpdateQuestionDTO(
            question_id="Q005",
            question_type=QuestionType.MATCH_PAIRS,
            question_text="Updated: Match pairs correctly",
            difficulty=Difficulty.MEDIUM,
            correct_pairs=[{"left": "HTML", "right": "Markup"}, {"left": "CSS", "right": "Style"}]
        ),
    ]

    updated_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="Updated: What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T001",
            correct_answer=["2"],
            created_at=now,
            updated_at=now,
            options=["3", "4"]
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Updated: Select even numbers",
            question_type=QuestionType.MCQ_MULTI,
            difficulty_level=Difficulty.HARD,
            topic_id="T002",
            correct_answer=["2", "3"],
            created_at=now,
            updated_at=now,
            options=["1", "2", "4"]
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Updated: Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T003",
            correct_answer=True,
            created_at=now,
            updated_at=now
        ),
        QuestionDTO(
            question_id="Q004",
            question_text="Updated: Fill the blank - Python is ____ language",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.EASY,
            topic_id="T004",
            correct_answer="interpreted",
            created_at=now,
            updated_at=now
        ),
        QuestionDTO(
            question_id="Q005",
            question_text="Updated: Match pairs correctly",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T005",
            correct_answer=[{"left": "HTML", "right": "Markup"}, {"left": "CSS", "right": "Style"}],
            created_at=now,
            updated_at=now
        ),
    ]

    storage.get_questions.return_value = updated_questions

    storage.update_questions.return_value = updated_questions

    # ACT
    result = interactor.update_questions(questions_to_update)

    # ASSERT
    storage.update_questions.assert_called_once_with(questions=questions_to_update)
    assert result == updated_questions

    snapshot.assert_match(repr(result), "test_update_questions_successfully")
