import pytest
from unittest.mock import create_autospec
from assessment.interactors.questions.get_questions_interactor import GetQuestionsInteractor
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionDTO, QuestionType, Difficulty
from assessment.exceptions.custom_exceptions import QuestionNotFound
from datetime import datetime


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return GetQuestionsInteractor(question_storage=storage)


def test_get_questions_successfully(interactor, storage, snapshot):
    # ARRANGE
    question_ids = ["Q001", "Q002"]

    expected_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
            topic_id="T001",
            correct_answer=["opt1"],
            options=["opt1", "opt2"],
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Is Python interpreted?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T002",
            correct_answer=True,
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        )
    ]

    storage.get_questions.return_value = expected_questions

    # ACT
    result = interactor.get_questions(question_ids=question_ids)

    # ASSERT
    assert storage.get_questions.call_count == 2
    storage.get_questions.assert_any_call(question_ids=question_ids)
    assert result == expected_questions
    snapshot.assert_match(repr(result), "test_get_questions_successfully")


def test_get_questions_raises_not_found(interactor, storage, snapshot):
    # ARRANGE
    question_ids = ["INVALID_QID"]
    storage.get_questions.side_effect = QuestionNotFound(["Question not found"])

    # ACT + ASSERT
    with pytest.raises(QuestionNotFound):
        interactor.get_questions(question_ids=question_ids)

    snapshot.assert_match(
        "QuestionNotFound raised for invalid question ids",
        "test_get_questions_raises_not_found"
    )
