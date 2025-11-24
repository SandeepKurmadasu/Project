import pytest
import uuid
from unittest.mock import create_autospec
from faker import Faker

from assessment.interactors.attempts_interactor.get_next_question_interactor import (
    GetNextQuestionInteractor
)
from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import (
    AttemptStorageInterface
)
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface
from course_management.interactors.dtos import StatusEnum

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
        fixed_user_id = "user-001"
        fixed_assessment_id = "assessment-001"

        # Use proper UUIDs for question IDs
        q1_id = str(uuid.UUID('11111111-1111-1111-1111-111111111111'))
        q2_id = str(uuid.UUID('22222222-2222-2222-2222-222222222222'))
        q3_id = str(uuid.UUID('33333333-3333-3333-3333-333333333333'))

        attempt_dto = AssessmentAttemptDTO(
            attempt_id=attempt_id,
            user_id=fixed_user_id,
            assessment_id=fixed_assessment_id,
            question_ids=[q1_id, q2_id, q3_id],
            total_points=0,
            status=StatusEnum.IN_PROGRESS,
            started_at=None
        )

        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            uuid.UUID(q1_id)]
        interactor.question_storage.get_questions.return_value = [
            MockQuestionDTO(q2_id, "Question 2", ["A", "B"])
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

        # Use proper UUIDs for question IDs
        q1_id = str(uuid.UUID('11111111-1111-1111-1111-111111111111'))
        q2_id = str(uuid.UUID('22222222-2222-2222-2222-222222222222'))

        attempt_dto = AssessmentAttemptDTO(
            attempt_id=attempt_id,
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=[q1_id, q2_id],
            total_points=0,
            status=StatusEnum.IN_PROGRESS,
            started_at=None
        )

        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            uuid.UUID(q1_id), uuid.UUID(q2_id)]

        expected_progress_dto = AssessmentAttemptDTO(
            attempt_id=attempt_id,
            total_points=50,
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=[],
            status=StatusEnum.COMPLETE,
            started_at=None
        )

        interactor.attempt_storage.complete_assessment_attempt.return_value = expected_progress_dto

        # Act
        result = interactor.get_next_question(attempt_id=attempt_id)

        # Assert
        snapshot.assert_match(repr(result), "assessment_completion.txt")

    def test_get_next_question_data_returns_unanswered(self, interactor):
        # Arrange
        attempt_id = "attempt-x"
        fixed_user_id = "user-002"
        fixed_assessment_id = "assessment-002"

        # Use proper UUIDs for question IDs
        q1_id = str(uuid.UUID('11111111-1111-1111-1111-111111111111'))
        q2_id = str(uuid.UUID('22222222-2222-2222-2222-222222222222'))
        q3_id = str(uuid.UUID('33333333-3333-3333-3333-333333333333'))

        attempt_dto = AssessmentAttemptDTO(
            attempt_id=attempt_id,
            user_id=fixed_user_id,
            assessment_id=fixed_assessment_id,
            question_ids=[q1_id, q2_id, q3_id],
            total_points=0,
            status=StatusEnum.IN_PROGRESS,
            started_at=None
        )

        interactor.attempt_storage.get_assessment_attempt.return_value = attempt_dto
        interactor.response_question_storage.get_answered_submission_questions.return_value = [
            uuid.UUID(q1_id), uuid.UUID(q3_id)]
        interactor.question_storage.get_questions.return_value = [
            MockQuestionDTO(q2_id, "Q2", ["A"])]

        # Act
        result = interactor.get_next_question_data(attempt_id)

        # Assert
        assert result.question_id == q2_id