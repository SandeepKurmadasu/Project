import pytest
from datetime import datetime
from unittest.mock import create_autospec
from pytest_snapshot.plugin import snapshot

from assessment.interactors.questions.add_questions_to_bank_interactor import AddQuestionsToBankInteractor
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO, QuestionDTO, QuestionType, Difficulty
from assessment.exceptions.custom_exceptions import (
    QuestionNotFound, QuestionBankNotFound
)
from django.core.exceptions import ObjectDoesNotExist


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return AddQuestionsToBankInteractor(storage=storage)


def test_add_questions_to_bank_successfully(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["Q001", "Q002", "Q003"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"

    )

    existing_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is 2+2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
            topic_id="T001",
            correct_answer=["opt1"],
            options=["opt1", "opt2", "opt3", "opt4"],
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Is Python interpreted?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T001",
            correct_answer=True,
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Fill in the blank: Python is ___",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.HARD,
            topic_id="T001",
            correct_answer="interpreted",
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        )
    ]

    updated_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=question_ids,
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    # Mock methods
    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = existing_questions
    storage.add_question_to_bank.return_value = updated_bank

    # ACT
    result = interactor.add_question(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert storage.get_question_bank.call_count == 2
    storage.get_questions.assert_called_once_with(question_ids)
    storage.add_question_to_bank.assert_called_once_with(bank_id=bank_id, question_ids=question_ids)
    assert result == updated_bank

    snapshot.assert_match(repr(result), "test_add_questions_to_bank_successfully")


def test_add_questions_raises_bank_not_found(interactor, storage):
    # ARRANGE
    bank_id = "INVALID_BANK"
    question_ids = ["Q001", "Q002"]

    storage.get_question_bank.side_effect = ObjectDoesNotExist()

    # ACT + ASSERT
    with pytest.raises(QuestionBankNotFound):
        interactor.add_question(bank_id=bank_id, question_ids=question_ids)

    storage.get_question_bank.assert_called_once_with(bank_id)
    storage.get_questions.assert_not_called()
    storage.add_question_to_bank.assert_not_called()

def test_add_questions_raises_questions_not_found(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["Q001", "INVALID_Q"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    # Only one question exists
    existing_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is 2+2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
            topic_id="T001",
            correct_answer=["opt1"],
            options=["opt1", "opt2", "opt3", "opt4"],
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        )
    ]

    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = existing_questions

    # ACT + ASSERT
    with pytest.raises(QuestionNotFound) as exc_info:
        interactor.add_question(bank_id=bank_id, question_ids=question_ids)

    assert exc_info.value.question_ids == ["INVALID_Q"]
    storage.add_question_to_bank.assert_not_called()

    snapshot.assert_match(repr(exc_info.value), "test_add_questions_raises_questions_not_found")


def test_add_single_question_to_bank(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["Q001"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    existing_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="Match the pairs",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T001",
            correct_answer=[{"left": "A", "right": "1"}, {"left": "B", "right": "2"}],
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        )
    ]

    updated_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=question_ids,
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = existing_questions
    storage.add_question_to_bank.return_value = updated_bank

    # ACT
    result = interactor.add_question(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert result == updated_bank
    assert len(result.question_ids) == 1

    snapshot.assert_match(repr(result), "test_add_single_question_to_bank")