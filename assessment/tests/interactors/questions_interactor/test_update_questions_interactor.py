import pytest
from unittest.mock import create_autospec

from assessment.interactors.questions.update_questions_interactor import UpdateQuestionInteractor
from assessment.interactors.dtos import UpdateQuestionDTO, QuestionDTO
from assessment.interactors.dtos import Difficulty, QuestionTypeDTO
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
            question_type=QuestionTypeDTO.MCQ_SINGLE,
            question_text="Updated: What is 2 + 2?",
            difficulty=Difficulty.MEDIUM,
            options=[{"1": "4"}, {"2": "5"}, {"3": "7"}],
            correct_answer=["2"]
        ),
        UpdateQuestionDTO(
            question_id="Q002",
            question_type=QuestionTypeDTO.MCQ_MULTI,
            question_text="Updated: Select even numbers",
            difficulty=Difficulty.HARD,
            options=[{"1": "1"}, {"2": "2"}, {"3":"4"}],
            correct_answer=["2", "3"]
        ),
        UpdateQuestionDTO(
            question_id="Q003",
            question_type=QuestionTypeDTO.TRUE_FALSE,
            question_text="Updated: Python is dynamically typed?",
            difficulty=Difficulty.MEDIUM,
            correct_answer=True
        ),
        UpdateQuestionDTO(
            question_id="Q004",
            question_type=QuestionTypeDTO.FILL_BLANK,
            question_text="Updated: Fill the blank - Python is ____ language",
            difficulty=Difficulty.EASY,
            correct_answer="interpreted"
        ),
        UpdateQuestionDTO(
            question_id="Q005",
            question_type=QuestionTypeDTO.MATCH_PAIRS,
            question_text="Updated: Match pairs correctly",
            difficulty=Difficulty.MEDIUM,
            options=[{"left_items":["HTML","CSS"]},{"right_items":["MARKUP","STYLE"]}],
            correct_answer=[
                [0, 0],
                [1, 1]
            ],
        ),
    ]

    updated_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="Updated: What is 2 + 2?",
            question_type=QuestionTypeDTO.MCQ_SINGLE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=["1"],
            options=[{"1": "4"}, {"2": "5"}, {"3": "7"}],
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Updated: Select even numbers",
            question_type=QuestionTypeDTO.MCQ_MULTI,
            difficulty_level=Difficulty.HARD,
            correct_answer=["1", "4"],
            options=[{"1":"2"},{"2":"7"},{"3":"5"},{"4":"6"}],
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Updated: Python is dynamically typed?",
            question_type=QuestionTypeDTO.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=True,
        ),
        QuestionDTO(
            question_id="Q004",
            question_text="Updated: Fill the blank - Python is ____ language",
            question_type=QuestionTypeDTO.FILL_BLANK,
            difficulty_level=Difficulty.EASY,
            correct_answer="interpreted",
        ),
        QuestionDTO(
            question_id="Q005",
            question_text="Updated: Match pairs correctly",
            question_type=QuestionTypeDTO.MATCH_PAIRS,
            difficulty_level=Difficulty.MEDIUM,
            options=[{"left_items": ["HTML", "CSS"]}, {"right_items": ["Markup", "Style"]}],
            correct_answer=[
                [0, 0],
                [1, 1]
            ],
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
