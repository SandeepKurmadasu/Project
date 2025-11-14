import pytest
from unittest.mock import create_autospec
from assessment.interactors.questionbank.reorder_questions_interactor import ReorderQuestionsInteractor
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.exceptions.custom_exceptions import QuestionBankNotFound, InvalidQuestionOrder



@pytest.fixture
def bank_storage():
    return create_autospec(QuestionBankStorageInterface)

@pytest.fixture
def interactor(bank_storage):
    return ReorderQuestionsInteractor(question_bank_storage=bank_storage)


def test_reorder_questions_successfully(interactor, bank_storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    ordered_question_ids = ["Q002", "Q001", "Q003"]

    existing_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Science Bank",
        question_ids=["Q001", "Q002", "Q003"],  # original order
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )

    expected_bank = QuestionBankDTO(
        bank_id=bank_id,
        name="Science Bank",
        question_ids=ordered_question_ids,
        created_at="2025-11-01",
        updated_at="2025-11-01"
    )


    bank_storage.get_question_bank.return_value = existing_bank
    bank_storage.reorder_questions_in_bank.return_value = expected_bank

    # ACT
    result = interactor.reorder_questions(bank_id=bank_id, ordered_question_ids=ordered_question_ids)

    # ASSERT
    assert bank_storage.get_question_bank.call_count == 2
    bank_storage.get_question_bank.assert_any_call(bank_id)
    bank_storage.reorder_questions_in_bank.assert_called_once_with(
        bank_id=bank_id, ordered_question_ids=ordered_question_ids
    )
    assert result == expected_bank
    snapshot.assert_match(repr(result), "test_reorder_questions_successfully")


def test_reorder_questions_raises_bank_not_found(interactor, bank_storage, snapshot):
    # ARRANGE
    bank_id = "INVALID_BANK"
    ordered_question_ids = ["Q001", "Q002"]

    bank_storage.get_question_bank.side_effect = QuestionBankNotFound(bank_id)

    # ACT + ASSERT
    with pytest.raises(QuestionBankNotFound):
        interactor.reorder_questions(bank_id=bank_id, ordered_question_ids=ordered_question_ids)

    snapshot.assert_match(
        "QuestionBankNotFound raised for invalid bank_id",
        "test_reorder_questions_raises_bank_not_found"
    )


def test_reorder_questions_raises_invalid_order(interactor, bank_storage, snapshot):
    # ARRANGE
    bank_id = "B001"
    ordered_question_ids = ["Q999"]

    bank_storage.reorder_questions_in_bank.side_effect = InvalidQuestionOrder(["Invalid question order"])

    # ACT + ASSERT
    with pytest.raises(InvalidQuestionOrder):
        interactor.reorder_questions(bank_id=bank_id, ordered_question_ids=ordered_question_ids)

    snapshot.assert_match(
        "InvalidQuestionOrder raised for invalid question order",
        "test_reorder_questions_raises_invalid_order"
    )
