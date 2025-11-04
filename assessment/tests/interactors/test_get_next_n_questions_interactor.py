import random

import pytest
from datetime import datetime
from unittest.mock import create_autospec

from assessment.interactors.question_scoring.get_next_n_questions_interactor import GetNextNQuestionsInteractor
from assessment.interactors.dtos import (
    SelectionConfigDTO,
    QuestionDTO,
    Difficulty,
    AttemptedQuestionDTO, QuestionType, Algorithm,
)
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


def make_questions():
    now = datetime(2025, 11, 1)
    return [
        QuestionDTO(
            question_id="q1",
            question_text="Easy Question 1",
            difficulty_level=Difficulty.EASY,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="A",
            topic_id="t1",
            created_at=now,
            updated_at=now,
        ),
        QuestionDTO(
            question_id="q2",
            question_text="Easy Question 2",
            difficulty_level=Difficulty.EASY,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="B",
            topic_id="t1",
            created_at=now,
            updated_at=now,
        ),
        QuestionDTO(
            question_id="q3",
            question_text="Medium Question 1",
            difficulty_level=Difficulty.MEDIUM,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="C",
            topic_id="t1",
            created_at=now,
            updated_at=now,
        ),
        QuestionDTO(
            question_id="q4",
            question_text="Hard Question 1",
            difficulty_level=Difficulty.HARD,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="D",
            topic_id="t1",
            created_at=now,
            updated_at=now,
        ),
        QuestionDTO(
            question_id="q5",
            question_text="Hard Question 2",
            difficulty_level=Difficulty.HARD,
            question_type=QuestionType.MCQ_SINGLE,
            correct_answer="A",
            topic_id="t1",
            created_at=now,
            updated_at=now,
        ),
    ]


@pytest.fixture
def mock_storage():
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(mock_storage):
    return GetNextNQuestionsInteractor(storage=mock_storage)

@pytest.fixture(autouse=True)
def reset_random():
    random.seed(42)
    yield
    random.seed()

def test_random_selection_returns_random_subset(interactor, mock_storage,snapshot):
    questions = make_questions()
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    mock_storage.get_question_bank.return_value = bank
    mock_storage.get_questions.return_value = questions

    config = SelectionConfigDTO(
        user_id="u1",
        question_bank_id="b1",
        number_of_questions=3,
        algorithm=Algorithm.RANDOM,
        difficulty_weights=None,
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)

    snapshot.assert_match(repr(result),"test_random_selection_returns_random_subset")

    assert len(result) == 3
    for q in result:
        assert q in questions


def test_difficulty_mix_selection_with_weights(interactor, mock_storage,snapshot):
    questions = make_questions()
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    mock_storage.get_question_bank.return_value = bank
    mock_storage.get_questions.return_value = questions

    config = SelectionConfigDTO(
        user_id="u1",
        question_bank_id="b1",
        number_of_questions=3,
        algorithm=Algorithm.DIFFICULTY_MIX,
        difficulty_weights={Difficulty.EASY: 1, Difficulty.MEDIUM: 1, Difficulty.HARD: 1},
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)
    snapshot.assert_match(repr(result),"test_difficulty_mix_selection_with_weights")

    assert len(result) == 3
    difficulties = [q.difficulty_level for q in result]
    assert Difficulty.EASY in difficulties
    assert Difficulty.MEDIUM in difficulties
    assert Difficulty.HARD in difficulties


def test_remove_already_attempted_questions(interactor, mock_storage,snapshot):
    questions = make_questions()
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    mock_storage.get_question_bank.return_value = bank
    mock_storage.get_questions.return_value = questions

    attempted = [AttemptedQuestionDTO(question_id="q1",is_correct="True")]
    config = SelectionConfigDTO(
        user_id="u1",
        question_bank_id="b1",
        number_of_questions=4,
        algorithm=Algorithm.RANDOM,
        difficulty_weights=None,
        already_attempted_questions=attempted,
    )

    result = interactor.get_questions(config)
    snapshot.assert_match(repr(result),"test_remove_already_attempted_questions")

    ids = [q.question_id for q in result]
    assert "q1" not in ids


def test_difficulty_mix_with_only_easy(interactor, mock_storage,snapshot):
    questions = make_questions()
    bank = type("Bank", (), {"question_ids": [q.question_id for q in questions]})
    mock_storage.get_question_bank.return_value = bank
    mock_storage.get_questions.return_value = questions

    config = SelectionConfigDTO(
        user_id="u1",
        question_bank_id="b1",
        number_of_questions=2,
        algorithm=Algorithm.DIFFICULTY_MIX,
        difficulty_weights={Difficulty.EASY: 2, Difficulty.MEDIUM: 0, Difficulty.HARD: 0},
        already_attempted_questions=None,
    )

    result = interactor.get_questions(config)
    snapshot.assert_match(repr(result),"test_difficulty_mix_with_only_easy")

    assert len(result) == 2
    for q in result:
        assert q.difficulty_level == Difficulty.EASY
