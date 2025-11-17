import pytest
from unittest.mock import create_autospec
from pytest_snapshot.plugin import snapshot

from assessment.interactors.questionbank.remove_question_from_bank_interactor import RemoveQuestionFromBankInteractor
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface

from assessment.interactors.dtos import (
    QuestionBankDTO,
    QuestionBankQuestionDTO,
    OrderedQuestionDTO,
    QuestionDTO,
    QuestionType,
    Difficulty
)
from assessment.exceptions.custom_exceptions import QuestionNotFound, QuestionBankNotFound
from django.core.exceptions import ObjectDoesNotExist


@pytest.fixture
def storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def bank_storage():
    return create_autospec(QuestionBankStorageInterface)


@pytest.fixture
def question_bank_question_storage():
    return create_autospec(QuestionBankQuestionStorageInterface)


@pytest.fixture
def interactor(storage, bank_storage, question_bank_question_storage):
    return RemoveQuestionFromBankInteractor(
        question_storage=storage,
        question_bank_storage=bank_storage,
        question_bank_question_storage=question_bank_question_storage,
    )


def test_remove_questions_from_bank_successfully(
        interactor, storage, bank_storage, question_bank_question_storage, snapshot):
    bank_id = "B001"
    question_ids = ["Q001", "Q002"]

    bank_storage.get_question_bank.return_value = QuestionBankDTO(
        bank_id=bank_id,
        name="Math Bank",
        assessment_id="S1",
        created_at="2025-11-01",
        updated_at="2025-11-01",
    )

    # VALID QuestionDTO objects
    storage.get_questions.return_value = [
        QuestionDTO(
            question_id="Q001",
            question_text="2+2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
            correct_answer=["opt1"],
            options=[{"1": "4"}, {"2": "5"}, {"3": "7"}]
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Is Python interpreted?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
            correct_answer=True
        )
    ]

    # Mock bank content
    question_bank_question_storage.get_bank_questions.return_value = [
        OrderedQuestionDTO("Q001", 1),
        OrderedQuestionDTO("Q002", 2),
        OrderedQuestionDTO("Q003", 3),
    ]

    updated_bank = QuestionBankQuestionDTO(
        bank_id=bank_id,
        questions=[OrderedQuestionDTO("Q003", 1)]
    )

    question_bank_question_storage.remove_question_from_bank.return_value = updated_bank

    result = interactor.remove_question_from_bank(bank_id, question_ids)

    assert result == updated_bank
    snapshot.assert_match(repr(result), "test_remove_questions_from_bank_successfully")


def test_remove_questions_raises_bank_not_found(
        interactor, storage, bank_storage, question_bank_question_storage):
    bank_id = "INVALID_BANK"
    question_ids = ["Q001"]

    bank_storage.get_question_bank.side_effect = ObjectDoesNotExist()

    with pytest.raises(QuestionBankNotFound):
        interactor.remove_question_from_bank(bank_id, question_ids)

    question_bank_question_storage.remove_question_from_bank.assert_not_called()


def test_remove_questions_raises_questions_not_found(
        interactor, storage, bank_storage, question_bank_question_storage, snapshot):
    bank_id = "B001"
    question_ids = ["INVALID_Q"]

    bank_storage.get_question_bank.return_value = QuestionBankDTO(
        bank_id=bank_id,
        name="Science Bank",
        assessment_id="K1",
        created_at="2025-11-01",
        updated_at="2025-11-01",
    )

    # No questions returned from DB → they don't exist
    storage.get_questions.return_value = []

    with pytest.raises(QuestionNotFound) as exc_info:
        interactor.remove_question_from_bank(bank_id, question_ids)

    assert exc_info.value.question_ids == ["INVALID_Q"]
    question_bank_question_storage.remove_question_from_bank.assert_not_called()

    snapshot.assert_match(repr(exc_info.value),
                          "test_remove_questions_raises_questions_not_found")


def test_remove_single_question_from_bank(
        interactor, storage, bank_storage, question_bank_question_storage, snapshot):
    bank_id = "B001"
    question_ids = ["Q001"]

    bank_storage.get_question_bank.return_value = QuestionBankDTO(
        bank_id="B001",
        name="Math Bank",
        assessment_id="S1",
        created_at="2025-11-01",
        updated_at="2025-11-01",
    )

    # VALID QuestionDTO object
    storage.get_questions.return_value = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is gravity?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.MEDIUM,
            options=[{"1":"A force that attracts objects toward each other"},
                     {"2":"A type of energy"},
                     {"3":"A form of light"},
                     {"4":"A chemical reaction"}],
            correct_answer=["1"],
        )
    ]

    # Bank contains Q001 and Q002
    question_bank_question_storage.get_bank_questions.return_value = [
        OrderedQuestionDTO("Q001", 1),
        OrderedQuestionDTO("Q002", 2)
    ]

    updated_bank = QuestionBankQuestionDTO(
        bank_id=bank_id,
        questions=[OrderedQuestionDTO("Q002", 1)]
    )

    question_bank_question_storage.remove_question_from_bank.return_value = updated_bank

    result = interactor.remove_question_from_bank(bank_id, question_ids)

    assert len(result.questions) == 1
    assert result.questions[0].question_id == "Q002"
    snapshot.assert_match(repr(result), "test_remove_single_question_from_bank")
