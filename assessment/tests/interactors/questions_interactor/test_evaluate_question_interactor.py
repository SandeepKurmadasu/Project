import pytest
from unittest.mock import Mock

from pytest_snapshot.plugin import snapshot

from assessment.interactors.evaluate_questions.evaluate_question_interactor import EvaluateQuestionInteractor
from assessment.interactors.dtos import QuestionDTO, QuestionTypeDTO, EvaluateQuestionDTO, Difficulty, AnswerStatus
from assessment.exceptions.custom_exceptions import QuestionNotFound


@pytest.fixture
def mock_storage():
    return Mock()


def test_evaluate_mcq_single_correct(mock_storage, snapshot):
    question = QuestionDTO(
        question_id="q1",
        question_text="2+2?",
        question_type=QuestionTypeDTO.MCQ_SINGLE,
        difficulty_level=Difficulty.EASY,
        options=[{"1": "4"}, {"2": "5"}, {"3": "7"}],
        correct_answer="4",
    )
    mock_storage.get_questions.return_value = [question]

    interactor = EvaluateQuestionInteractor(mock_storage)
    result = interactor.evaluate("q1", "4")

    snapshot.assert_match(repr(result), "mcq_single_result")

    assert isinstance(result, EvaluateQuestionDTO)
    assert result.is_correct == AnswerStatus.CORRECT


def test_evaluate_mcq_multi_correct(mock_storage, snapshot):
    question = QuestionDTO(
        question_id="q2",
        question_text="Select even numbers",
        question_type=QuestionTypeDTO.MCQ_MULTI,
        difficulty_level=Difficulty.MEDIUM,
        options=[{"1": "2"}, {"2": "7"}, {"3": "5"}, {"4": "6"}],
        correct_answer=["1", "4"],  # option IDs as list
    )
    mock_storage.get_questions.return_value = [question]

    interactor = EvaluateQuestionInteractor(mock_storage)

    # Pass the user answer as a list of option IDs, matching the expected format
    result = interactor.evaluate("q2", ["1", "4"])

    snapshot.assert_match(repr(result), "mcq_multi_result")

    assert result.is_correct == AnswerStatus.CORRECT





def test_evaluate_true_false_correct(mock_storage, snapshot):
    question = QuestionDTO(
        question_id="q3",
        question_text="The earth is round",
        question_type=QuestionTypeDTO.TRUE_FALSE,
        difficulty_level=Difficulty.EASY,
        correct_answer="true",
    )
    mock_storage.get_questions.return_value = [question]

    interactor = EvaluateQuestionInteractor(mock_storage)
    result = interactor.evaluate("q3", "True")

    snapshot.assert_match(repr(result), "true_false_result")

    assert result.is_correct == AnswerStatus.CORRECT


def test_evaluate_fill_in_blank_correct(mock_storage, snapshot):
    question = QuestionDTO(
        question_id="q4",
        question_text="Capital of India?",
        question_type=QuestionTypeDTO.FILL_BLANK,
        difficulty_level=Difficulty.EASY,
        correct_answer="New Delhi",
    )
    mock_storage.get_questions.return_value = [question]

    interactor = EvaluateQuestionInteractor(mock_storage)
    result = interactor.evaluate("q4", " new delhi ")

    snapshot.assert_match(repr(result), "fill_in_the_blank")

    assert result.is_correct == AnswerStatus.CORRECT


def test_evaluate_match_pairs_correct(mock_storage, snapshot):
    question = QuestionDTO(
        question_id="q5",
        question_text="Match capitals",
        question_type=QuestionTypeDTO.MATCH_PAIRS,
        difficulty_level=Difficulty.HARD,
        correct_answer={"India": "Delhi", "USA": "Washington"},  # Dictionary format
    )
    mock_storage.get_questions.return_value = [question]

    interactor = EvaluateQuestionInteractor(mock_storage)

    # Pass user answer as dictionary with matching key-value pairs
    result = interactor.evaluate("q5", {"India": "Delhi", "USA": "Washington"})

    snapshot.assert_match(repr(result), "match_pairs_result")

    assert result.is_correct == AnswerStatus.CORRECT


def test_question_not_found_raises_error(mock_storage):
    mock_storage.get_questions.side_effect = QuestionNotFound(["invalid_id"])

    interactor = EvaluateQuestionInteractor(mock_storage)

    with pytest.raises(QuestionNotFound):
        interactor.evaluate("invalid_id", "4")
