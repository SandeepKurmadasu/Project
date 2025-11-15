import pytest
from assessment.interactors.questions.create_questions_interactor import CreateQuestionsInteractor
from assessment.interactors.dtos import CreateQuestionDTO, QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.dtos import QuestionType, Difficulty


@pytest.fixture
def storage():
    # simple autospec to match interface
    from unittest.mock import create_autospec
    return create_autospec(QuestionStorageInterface)


@pytest.fixture
def interactor(storage):
    return CreateQuestionsInteractor(question_storage=storage)


def test_create_questions_successfully_for_all_types(interactor, storage, snapshot):

    questions = [

        CreateQuestionDTO(
            question_text="What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty=Difficulty.EASY,
            options=[{"id": "1", "text": "2"}, {"id": "2", "text": "4"}],
            correct_option_ids=["2"]
        ),

        CreateQuestionDTO(
            question_text="Select programming languages.",
            question_type=QuestionType.MCQ_MULTI,
            difficulty=Difficulty.MEDIUM,
            options=[{"id": "1", "text": "Python"}, {"id": "2", "text": "C++"}, {"id": "3", "text": "HTML"}],
            correct_option_ids=["1", "2"]
        ),
        CreateQuestionDTO(
            question_text="Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty=Difficulty.MEDIUM,
            correct_boolean=True
        ),
        CreateQuestionDTO(
            question_text="_____ is the capital of France.",
            question_type=QuestionType.FILL_BLANK,
            difficulty=Difficulty.EASY,
            correct_fill_text="Paris"
        ),
        CreateQuestionDTO(
            question_text="Match the countries with capitals.",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty=Difficulty.HARD,
            left_items=["France", "Japan"],
            right_items = ["Paris", "Tokyo"],
            correct_pairs = [
            [0, 0],
            [1, 1]
            ]
        )
    ]

    expected_questions = [
        QuestionDTO(
            question_id="Q001",
            question_text="What is 2 + 2?",
            question_type=QuestionType.MCQ_SINGLE,
            difficulty_level=Difficulty.EASY,
                   correct_answer=["2"],


            options=["2", "4"]
        ),
        QuestionDTO(
            question_id="Q002",
            question_text="Select programming languages.",
            question_type=QuestionType.MCQ_MULTI,
            difficulty_level=Difficulty.MEDIUM,
                   correct_answer=["1", "2"],


            options=["Python", "C++", "HTML"]
        ),
        QuestionDTO(
            question_id="Q003",
            question_text="Python is dynamically typed?",
            question_type=QuestionType.TRUE_FALSE,
            difficulty_level=Difficulty.MEDIUM,
                   correct_answer=True,

                    ),
        QuestionDTO(
            question_id="Q004",
            question_text="_____ is the capital of France.",
            question_type=QuestionType.FILL_BLANK,
            difficulty_level=Difficulty.EASY,
                   correct_answer="Paris",

                    ),
        QuestionDTO(
            question_id="Q005",
            question_text="Match the countries with capitals.",
            question_type=QuestionType.MATCH_PAIRS,
            difficulty_level=Difficulty.HARD,
                   correct_answer=[
                {"left": "France", "right": "Paris"},
                {"left": "Japan", "right": "Tokyo"}
            ],

                    ),
    ]

    storage.create_questions.return_value = expected_questions

    # ACT
    result = interactor.create_questions(questions)

    # ASSERT
    storage.create_questions.assert_called_once()
    assert result == expected_questions
    snapshot.assert_match(repr(result), "test_create_questions_successfully_for_all_types")
