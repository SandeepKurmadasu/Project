import pytest
from unittest.mock import create_autospec

from pytest_snapshot.plugin import snapshot

from assessment.interactors.questions.create_question_bank_interactor import CreateQuestionBankInteractor
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionBankDTO
from assessment.exceptions.custom_exceptions import DuplicateBankNameFound


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return CreateQuestionBankInteractor(storage=storage)


def test_create_question_bank_successfully(interactor, storage,snapshot):
    # ARRANGE
    name = "Math Bank"
    expected_bank = QuestionBankDTO(
        bank_id="B001",
        name=name,
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    # Mock methods
    storage.get_all_question_banks.return_value = []
    storage.create_question_bank.return_value = expected_bank

    # ACT
    result = interactor.create_question_bank(name)

    # ASSERT
    storage.get_all_question_banks.assert_called_once()
    storage.create_question_bank.assert_called_once_with(name=name)
    assert result == expected_bank

    snapshot.assert_match(repr(result),"test_create_question_bank_successfully")


def test_create_question_bank_raises_duplicate_name(interactor, storage,snapshot):
    # ARRANGE
    name = "Math Bank"
    existing_bank = QuestionBankDTO(
        bank_id="B002",
        name=name,
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    storage.get_all_question_banks.return_value = [existing_bank]

    # ACT + ASSERT
    with pytest.raises(DuplicateBankNameFound) as exc_info:
        interactor.create_question_bank(name)

    assert exc_info.value.name == name
    storage.create_question_bank.assert_not_called()

    snapshot.assert_match(repr(exc_info.value),"test_create_question_bank_raises_duplicate_name")
