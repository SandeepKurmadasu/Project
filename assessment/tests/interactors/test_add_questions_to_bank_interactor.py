import pytest
from unittest.mock import create_autospec
from pytest_snapshot.plugin import snapshot

from assessment.interactors.questionbank.add_questions_to_bank_interactor import AddQuestionsToBankInteractor
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.dtos import QuestionBankDTO, QuestionDTO, QuestionType, Difficulty
from assessment.exceptions.custom_exceptions import (
    QuestionNotFound, QuestionBankNotFound
)
from django.core.exceptions import ObjectDoesNotExist

from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


@pytest.fixture
def bank_storage():
    return create_autospec(QuestionBankStorageInterface)

@pytest.fixture
def question_storage():
    return create_autospec(QuestionStorageInterface)

@pytest.fixture
def question_bank_question_storage():
    return create_autospec(QuestionBankQuestionStorageInterface)

@pytest.fixture
def interactor(bank_storage, question_storage, question_bank_question_storage):
    return AddQuestionsToBankInteractor(question_storage= question_storage, question_bank_storage=bank_storage, question_bank_question_storage=question_bank_question_storage)


def test_add_questions_to_bank_successfully(interactor, question_storage, bank_storage, question_bank_question_storage, snapshot):
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
            correct_answer=["opt1"],
            options=["opt1", "opt2", "opt3", "opt4"],
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Is Python interpreted?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=True,
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Fill in the blank: Python is ___",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.HARD,
            correct_answer="interpreted",
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
    bank_storage.get_question_bank.return_value = existing_bank
    question_storage.get_questions.return_value = existing_questions
    question_bank_question_storage.add_questions_to_bank_ordered.return_value = updated_bank

    # ACT
    result = interactor.add_questions_to_bank(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert bank_storage.get_question_bank.call_count == 2
    question_storage.get_questions.assert_called_once_with(question_ids)

    question_bank_question_storage.add_questions_to_bank_ordered.assert_called_once_with(
        bank_id=bank_id,
        ordered_ids=[
            {"question_id": "Q001", "position": 1},
            {"question_id": "Q002", "position": 2},
            {"question_id": "Q003", "position": 3},
        ]
    )

    assert result == updated_bank

    snapshot.assert_match(repr(result), "test_add_questions_to_bank_successfully")


def test_add_questions_raises_bank_not_found(interactor, bank_storage, question_bank_question_storage, question_storage):
    # ARRANGE
    bank_id = "INVALID_BANK"
    question_ids = ["Q001", "Q002"]

    bank_storage.get_question_bank.side_effect = ObjectDoesNotExist()

    # ACT + ASSERT
    with pytest.raises(QuestionBankNotFound):
        interactor.add_questions_to_bank(bank_id=bank_id, question_ids=question_ids)

    bank_storage.get_question_bank.assert_called_once_with(bank_id)
    question_storage.get_questions.assert_not_called()
    question_bank_question_storage.add_questions_to_bank_ordered.assert_not_called()

def test_add_questions_raises_questions_not_found(interactor, question_storage, bank_storage, question_bank_question_storage, snapshot):
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
            correct_answer=["opt1"],
            options=["opt1", "opt2", "opt3", "opt4"],
        )
    ]

    bank_storage.get_question_bank.return_value = existing_bank
    question_storage.get_questions.return_value = existing_questions

    # ACT + ASSERT
    with pytest.raises(QuestionNotFound) as exc_info:
        interactor.add_questions_to_bank(bank_id=bank_id, question_ids=question_ids)

    assert exc_info.value.question_ids == ["INVALID_Q"]
    question_bank_question_storage.add_questions_to_bank_ordered.assert_not_called()

    snapshot.assert_match(repr(exc_info.value), "test_add_questions_raises_questions_not_found")


def test_add_single_question_to_bank(interactor, bank_storage, question_storage, question_bank_question_storage, snapshot):
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
            correct_answer=[{"left": "A", "right": "1"}, {"left": "B", "right": "2"}],
        )
    ]

    updated_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=question_ids,
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    bank_storage.get_question_bank.return_value = existing_bank
    question_storage.get_questions.return_value = existing_questions
    question_bank_question_storage.add_questions_to_bank_ordered.return_value = updated_bank

    # ACT
    result = interactor.add_questions_to_bank(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert result == updated_bank
    assert len(result.question_ids) == 1

    snapshot.assert_match(repr(result), "test_add_single_question_to_bank")