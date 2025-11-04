import pytest
from datetime import datetime
from unittest.mock import create_autospec
from pytest_snapshot.plugin import snapshot

from assessment.interactors.questionbank.remove_question_from_bank_interactor import RemoveQuestionFromBankInteractor
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO, QuestionDTO, QuestionType, Difficulty
from assessment.exceptions.custom_exceptions import QuestionNotFound, QuestionBankNotFound
from django.core.exceptions import ObjectDoesNotExist


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return RemoveQuestionFromBankInteractor(question_storage=storage)


def test_remove_questions_from_bank_successfully(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["Q001", "Q002"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=["Q001", "Q002", "Q003"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    updated_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        question_ids=["Q003"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = [
        QuestionDTO(
            question_id="Q001",
            question_text="2 + 2 = ?",
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
        topic_id="T001",
        correct_answer=True,
        created_at=datetime(2025, 11, 1),
        updated_at=datetime(2025, 11, 1)
    )
    ]
    storage.remove_question_from_bank.return_value = updated_bank

    # ACT
    result = interactor.remove_question_from_bank(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert storage.get_question_bank.call_count >= 1
    storage.get_question_bank.assert_any_call(bank_id)
    storage.remove_question_from_bank.assert_called_once_with(bank_id=bank_id, question_ids=question_ids)
    assert result == updated_bank

    snapshot.assert_match(repr(result), "test_remove_questions_from_bank_successfully")


def test_remove_questions_raises_bank_not_found(interactor, storage):
    # ARRANGE
    bank_id = "INVALID_BANK"
    question_ids = ["Q001"]

    storage.get_question_bank.side_effect = ObjectDoesNotExist()

    # ACT + ASSERT
    with pytest.raises(QuestionBankNotFound):
        interactor.remove_question_from_bank(bank_id=bank_id, question_ids=question_ids)

    storage.remove_question_from_bank.assert_not_called()


def test_remove_questions_raises_questions_not_found(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["INVALID_Q"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Science Bank",
        question_ids=["Q001", "Q002"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = []  # No valid questions

    # ACT + ASSERT
    with pytest.raises(QuestionNotFound) as exc_info:
        interactor.remove_question_from_bank(bank_id=bank_id, question_ids=question_ids)

    assert exc_info.value.question_ids == ["INVALID_Q"]
    storage.remove_question_from_bank.assert_not_called()

    snapshot.assert_match(repr(exc_info.value), "test_remove_questions_raises_questions_not_found")


def test_remove_single_question_from_bank(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    question_ids = ["Q001"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Physics Bank",
        question_ids=["Q001", "Q002"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    updated_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Physics Bank",
        question_ids=["Q002"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_question_bank.return_value = existing_bank
    storage.get_questions.return_value = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is gravity?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.MEDIUM,
            topic_id="T001",
            correct_answer=["opt1"],
            options=["opt1", "opt2"],
            created_at=datetime(2025, 11, 1),
            updated_at=datetime(2025, 11, 1)
        )
    ]
    storage.remove_question_from_bank.return_value = updated_bank

    # ACT
    result = interactor.remove_question_from_bank(bank_id=bank_id, question_ids=question_ids)

    # ASSERT
    assert result == updated_bank
    assert len(result.question_ids) == 1

    snapshot.assert_match(repr(result), "test_remove_single_question_from_bank")
