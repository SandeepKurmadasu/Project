import pytest
from unittest.mock import create_autospec

from faker import Faker

from cyber_edu_verse.assessment.exceptions.custom_exceptions import \
    AttemptIdNotFound, \
    AssessmentIdNotFound
from cyber_edu_verse.assessment.interactors.attempts_interactor.get_next_question_interactor import \
    GetNextQuestionInteractor
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface
from cyber_edu_verse.assessment.tests.factories.interactor_factories import \
    AssessmentAttemptDTOFactory

Faker.seed(1)


class MockQuestionDTO:
    def __init__(self, question_id, question_text, options):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options


class MockAssessmentDTO:
    def __init__(self, questions):
        self.questions = questions


@pytest.fixture
def interactor():
    assessment_storage = create_autospec(AssessmentStorageInterface)
    attempt_storage = create_autospec(AttemptStorageInterface)
    question_storage = create_autospec(QuestionStorageInterface)
    response_question_storage = create_autospec(
        AttemptSubmittedQuestionStorageInterface)

    return GetNextQuestionInteractor(
        assessment_storage=assessment_storage,
        attempt_storage=attempt_storage,
        question_storage=question_storage,
        response_question_storage=response_question_storage
    )


class TestGetNextQuestionInteractor:

    def test_get_next_question_when_remaining_questions_exist(self, interactor,
                                                              snapshot):
        # Arrange
        attempt_id = "attempt1"
        assessment_id = "assessment1"

        all_questions = [MockQuestionDTO(f"q{i}", f"Question {i}",
                                         [f"A", f"B"]) for i
                         in range(1, 4)]
        interactor.assessment_storage.get_assessment.return_value = MockAssessmentDTO(
            questions=all_questions)

        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1"]

        interactor.question_storage.get_questions.return_value = [
            MockQuestionDTO("q2", "Question 2", ["A", "B"])
        ]

        # Act
        result = interactor.get_next_question(attempt_id=attempt_id,
                                              assessment_id=assessment_id)

        # Assert

        snapshot.assert_match(repr(result), "display_question.txt")

    def test_get_next_question_when_no_remaining_questions(self, interactor,
                                                           snapshot):
        # Arrange
        attempt_id = "attempt1"
        assessment_id = "assessment1"
        user_id = "user_123"

        all_questions = [MockQuestionDTO("q1", "Q1", []),
                         MockQuestionDTO("q2", "Q2", [])]
        interactor.assessment_storage.get_assessment.return_value = MockAssessmentDTO(
            questions=all_questions)

        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1", "q2"]

        expected_progress_dto = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            assessment_id=assessment_id,
            user_id=user_id,
            total_points=50
        )
        interactor.attempt_storage.complete_assessment_attempt.return_value = expected_progress_dto

        # Act
        result = interactor.get_next_question(attempt_id=attempt_id,
                                              assessment_id=assessment_id)

        # Assert

        snapshot.assert_match(repr(result), "assessment_completion.txt")

    def test_get_remaining_questions_logic(self, interactor):
        assessment_id = "a1"
        attempt_id = "attempt-x"

        interactor.assessment_storage.get_assessment.return_value = MockAssessmentDTO(
            questions=[MockQuestionDTO("q1", "", []),
                       MockQuestionDTO("q2", "", []),
                       MockQuestionDTO("q3", "", [])]
        )

        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1", "q3"]

        remaining = interactor.get_next_question_data(assessment_id,
                                                      attempt_id)

        assert remaining.question_id == "q2"

    def test_get_next_question_assessment_not_found(self, interactor):
        interactor.assessment_storage.get_assessment.side_effect = AssessmentIdNotFound(
            "Assessment not found")

        with pytest.raises(AssessmentIdNotFound):
            interactor.get_next_question(attempt_id="a1",
                                         assessment_id="invalid-assessment")

    def test_get_next_question_attempt_not_found(self, interactor):
        interactor.assessment_storage.get_assessment.return_value = type(
            "A", (), {"questions": []}
        )
        interactor.response_question_storage.get_answered_submission_questions.side_effect = AttemptIdNotFound(
            "Attempt missing")

        with pytest.raises(AttemptIdNotFound):
            interactor.get_next_question(attempt_id="invalid-attempt",
                                         assessment_id="a1")
