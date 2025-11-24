import random

import pytest
from unittest.mock import create_autospec

from assessment.interactors.question_selection.get_next_n_questions_interactor import GetNextNQuestionsInteractor
from assessment.interactors.dtos import (
    SelectionConfigDTO,
    QuestionDTO,
    Difficulty,
    QuestionType, Algorithm,
)
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


def make_questions():
    return [
        QuestionDTO(
            question_id="q1",
            question_text="Easy Question 1",
            difficulty_level=Difficulty.EASY,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="A",
            ),
        QuestionDTO(
            question_id="q2",
            question_text="Easy Question 2",
            difficulty_level=Difficulty.EASY,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="B",
            ),
        QuestionDTO(
            question_id="q3",
            question_text="Medium Question 1",
            difficulty_level=Difficulty.MEDIUM,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="C",
            ),
        QuestionDTO(
            question_id="q4",
            question_text="Hard Question 1",
            difficulty_level=Difficulty.HARD,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="D",
            ),
        QuestionDTO(
            question_id="q5",
            question_text="Hard Question 2",
            difficulty_level=Difficulty.HARD,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="A",
            ),
    ]


@pytest.fixture
def question_storage_mock():
    return create_autospec(QuestionStorageInterface, instance=True)

@pytest.fixture
def question_bank_storage_mock():
    return create_autospec(QuestionBankStorageInterface, instance=True)

@pytest.fixture
def question_bank_question_storage_mock():
    return create_autospec(QuestionBankQuestionStorageInterface, instance=True)

@pytest.fixture
def interactor(
    question_storage_mock,
    question_bank_storage_mock,
    question_bank_question_storage_mock,
):
    return GetNextNQuestionsInteractor(
        question_storage=question_storage_mock,
        question_bank_storage=question_bank_storage_mock,
        question_bank_question_storage=question_bank_question_storage_mock,
    )

@pytest.fixture(autouse=True)
def reset_random():
    random.seed(42)
    yield
    random.seed()

def test_random_selection_returns_random_subset(
    interactor,
    question_storage_mock,
    snapshot
):
    questions = make_questions()

    # Mock question bank containing question IDs
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})

    # 1. Question bank returns a bank object
    interactor.question_bank_storage.get_question_bank.return_value = bank

    # 2. Question storage returns actual QuestionDTO list
    question_storage_mock.get_questions.return_value = questions

    config = SelectionConfigDTO(
        question_bank_id="b1",
        number_of_questions=3,
        algorithm=Algorithm.RANDOM,
        difficulty_weights=None,
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)

    snapshot.assert_match(repr(result), "test_random_selection_returns_random_subset")

    assert len(result) == 3
    for q in result:
        assert q in questions



def test_difficulty_mix_selection_with_weights(
    interactor,
    question_storage_mock,
    snapshot
):
    questions = make_questions()

    # Mock bank with question IDs
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    interactor.question_bank_storage.get_question_bank.return_value = bank

    # Mock storage returning actual question objects
    question_storage_mock.get_questions.return_value = questions

    config = SelectionConfigDTO(
        question_bank_id="b1",
        number_of_questions=3,
        algorithm=Algorithm.DIFFICULTY_MIX,
        difficulty_weights={
            Difficulty.EASY: 1,
            Difficulty.MEDIUM: 1,
            Difficulty.HARD: 1
        },
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)
    snapshot.assert_match(repr(result), "test_difficulty_mix_selection_with_weights")

    assert len(result) == 3
    difficulties = [q.difficulty_level for q in result]

    assert Difficulty.EASY in difficulties
    assert Difficulty.MEDIUM in difficulties
    assert Difficulty.HARD in difficulties



def test_remove_already_attempted_questions(
    interactor,
    question_storage_mock,
    snapshot
):
    questions = make_questions()

    # Mock bank with question IDs
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    interactor.question_bank_storage.get_question_bank.return_value = bank

    # Mock storage returning actual question objects
    question_storage_mock.get_questions.return_value = questions

    config = SelectionConfigDTO(
        question_bank_id="b1",
        number_of_questions=4,
        algorithm=Algorithm.RANDOM,
        difficulty_weights=None,
        already_attempted_questions=["q1"],  # remove q1
    )

    result = interactor.get_questions(config)


    snapshot.assert_match(repr(result), "test_remove_already_attempted_questions")


def test_difficulty_mix_with_only_easy(
    interactor,
    question_storage_mock,
    snapshot
):
    questions = make_questions()

    # Mock bank with question IDs
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    interactor.question_bank_storage.get_question_bank.return_value = bank

    # Mock storage returning actual question objects
    question_storage_mock.get_questions.return_value = questions

    config = SelectionConfigDTO(
        question_bank_id="b1",
        number_of_questions=2,
        algorithm=Algorithm.DIFFICULTY_MIX,
        difficulty_weights={
            Difficulty.EASY: 2,
            Difficulty.MEDIUM: 0,
            Difficulty.HARD: 0
        },
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)

    snapshot.assert_match(repr(result), "test_difficulty_mix_with_only_easy")

    assert len(result) == 2
    for q in result:
        assert q.difficulty_level == Difficulty.EASY
