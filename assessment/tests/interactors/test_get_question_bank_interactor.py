import pytest
from unittest.mock import create_autospec
from pytest_snapshot.plugin import snapshot

from assessment.interactors.questionbank.get_question_bank_interactor import GetQuestionBankInteractor
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.dtos import QuestionBankDTO
from assessment.exceptions.custom_exceptions import QuestionBankNotFound


@pytest.fixture
def storage():
    return create_autospec(QuestionBankStorageInterface)


@pytest.fixture
def interactor(storage):
    return GetQuestionBankInteractor(storage=storage)


def test_get_question_bank_successfully(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    expected_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Science Bank",
        question_ids=["Q001", "Q002"],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_question_bank.return_value = expected_bank

    # ACT
    result = interactor.get_question_bank(bank_id=bank_id)

    # ASSERT
    assert storage.get_question_bank.call_count == 2
    storage.get_question_bank.assert_any_call(bank_id)
    assert result == expected_bank

    snapshot.assert_match(repr(result), "test_get_question_bank_successfully")


def test_get_question_bank_raises_not_found(interactor, storage, snapshot):
    # ARRANGE
    bank_id = "INVALID_BANK"
    storage.get_question_bank.side_effect = QuestionBankNotFound(bank_id=bank_id)

    # ACT + ASSERT
    with pytest.raises(QuestionBankNotFound) as exc_info:
        interactor.get_question_bank(bank_id=bank_id)

    storage.get_question_bank.assert_called_once_with(bank_id)
    snapshot.assert_match(repr(exc_info.value), "test_get_question_bank_raises_not_found")
