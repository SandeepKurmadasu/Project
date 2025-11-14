import pytest
from unittest.mock import create_autospec

from pytest_snapshot.plugin import snapshot

from assessment.interactors.questionbank.create_question_bank_interactor import CreateQuestionBankInteractor
from assessment.interactors.storage_interface.assessments_storage_interface import AssessmentStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.dtos import QuestionBankDTO
from assessment.exceptions.custom_exceptions import DuplicateBankNameFound



@pytest.fixture
def bank_storage():
    return create_autospec(QuestionBankStorageInterface)

@pytest.fixture
def assessment_storage():
    return create_autospec(AssessmentStorageInterface)


@pytest.fixture
def interactor(bank_storage,assessment_storage):
    return CreateQuestionBankInteractor(question_bank_storage=bank_storage,assessment_storage=assessment_storage)


def test_create_question_bank_successfully(interactor, bank_storage,snapshot):
    # ARRANGE
    name = "Math Bank"
    assessment_id = "Assessment-1"
    expected_bank = QuestionBankDTO(
        bank_id="B001",
        name=name,
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    # Mock methods
    bank_storage.get_question_bank_by_name.return_value = None
    bank_storage.create_question_bank_for_assessment.return_value = expected_bank

    # ACT
    result = interactor.create_question_bank(name,assessment_id)

    # ASSERT
    bank_storage.get_question_bank_by_name.assert_called_once_with(name=name)
    assert result == expected_bank

    snapshot.assert_match(repr(result),"test_create_question_bank_successfully")


def test_create_question_bank_raises_duplicate_name(interactor, bank_storage,snapshot):
    # ARRANGE
    name = "Math Bank"
    assessment_id = "B1"
    existing_bank = QuestionBankDTO(
        bank_id="B002",
        name=name,
        question_ids=[],
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    bank_storage.get_question_bank_by_name.return_value = existing_bank

    # ACT + ASSERT
    with pytest.raises(DuplicateBankNameFound) as exc_info:

        interactor.create_question_bank(name,assessment_id)

    assert exc_info.value.name == name

    snapshot.assert_match(repr(exc_info.value),"test_create_question_bank_raises_duplicate_name")
