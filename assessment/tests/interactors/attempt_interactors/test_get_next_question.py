import pytest
from unittest.mock import create_autospec
from faker import Faker

from assessment.interactors.attempts_interactor.get_next_question_interactor import (
    GetNextQuestionInteractor
)
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import (
    AttemptStorageInterface
)
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface
from assessment.tests.factories.factories import AssessmentAttemptDTOFactory

Faker.seed(1)


class MockQuestionDTO:
    def __init__(self, question_id, question_text, options):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options


@pytest.fixture
def interactor():
    attempt_storage = create_autospec(AttemptStorageInterface)
    question_storage = create_autospec(QuestionStorageInterface)
    response_question_storage = create_autospec(
        AttemptSubmittedQuestionStorageInterface)

    return GetNextQuestionInteractor(
        attempt_storage=attempt_storage,
        question_storage=question_storage,
        response_question_storage=response_question_storage
    )


class TestGetNextQuestionInteractor:

    def test_get_next_question_when_remaining_questions_exist(self, interactor,
                                                              snapshot):
        # Arrange
        attempt_id = "attempt1"
        attempt_dto = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            question_ids=["q1", "q2", "q3"]
        )
        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1"]
        interactor.question_storage.get_questions.return_value = [
            MockQuestionDTO("q2", "Question 2", ["A", "B"])
        ]

        # Act
        result = interactor.get_next_question(attempt_id=attempt_id)

        # Assert
        snapshot.assert_match(repr(result), "display_question.txt")

    def test_get_next_question_when_no_remaining_questions(self, interactor,
                                                           snapshot):
        # Arrange
        attempt_id = "attempt1"
        user_id = "user1"
        assessment_id = "assessment_id1"
        attempt_dto = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=["q1", "q2"]
        )
        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1", "q2"]

        expected_progress_dto = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            total_points=50,
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=[]
        )
        interactor.attempt_storage.complete_assessment_attempt.return_value = expected_progress_dto

        # Act
        result = interactor.get_next_question(attempt_id=attempt_id)

        # Assert
        snapshot.assert_match(repr(result), "assessment_completion.txt")

    def test_get_next_question_data_returns_unanswered(self, interactor):
        # Arrange
        attempt_id = "attempt-x"
        attempt_dto = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            question_ids=["q1", "q2", "q3"]
        )
        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            "q1", "q3"]
        interactor.question_storage.get_questions.return_value = [
            MockQuestionDTO("q2", "Q2", ["A"])]

        # Act
        result = interactor.get_next_question_data(attempt_id)

        # Assert
        assert result.question_id == "q2"
