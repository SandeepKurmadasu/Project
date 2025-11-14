import pytest
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
            left_items=["HTML", "CSS"],
            right_items=["Markup", "Style"],
            correct_pairs=[
                [0, 0],
                [1, 1]
            ],
        ),
    ]

    updated_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="Updated: What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=["2"],
            options=["3", "4"]
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Updated: Select even numbers",
            question_type=QuestionType.MCQ_MULTI,
            difficulty_level=Difficulty.HARD,
            correct_answer=["2", "3"],
            options=["1", "2", "4"]
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Updated: Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=True,
        ),
        QuestionDTO(
            question_id="Q004",
            question_text="Updated: Fill the blank - Python is ____ language",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.EASY,
            correct_answer="interpreted",
        ),
        QuestionDTO(
            question_id="Q005",
            question_text="Updated: Match pairs correctly",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=[{"left": "HTML", "right": "Markup"}, {"left": "CSS", "right": "Style"}],
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
