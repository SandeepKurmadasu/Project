import pytest
from unittest.mock import create_autospec, patch, MagicMock
from assessment.exceptions.custom_exceptions import AssessmentIdNotFound
from assessment.interactors.attempts_interactor.start_assessment_attempt_interactor import StartAssessmentAttemptInteractor
from assessment.interactors.dtos import Algorithm, AssessmentAttemptDTO, \
    Difficulty
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import AssessmentStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.tests.factories.factories import QuestionDTOFactory
from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.interactors.storage_interfaces.user_storage_interface import UserStorageInterface


class TestStartAssessmentAttemptInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.assessments_storage = create_autospec(AssessmentStorageInterface)
        self.question_storage = create_autospec(QuestionStorageInterface)

        self.interactor = StartAssessmentAttemptInteractor(
            attempt_storage=self.attempt_storage,
            user_storage=self.user_storage,
            assessments_storage=self.assessments_storage,
            question_bank_storage=self.question_storage
        )

    def test_start_assessment_attempt_success(self, snapshot):
        # Arrange
        user_id = "user-001"
        assessment_id = "assess-123"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.return_value = True

        mock_assessment = MagicMock()
        mock_assessment.bank_id = "bank-001"
        mock_assessment.no_of_questions = 3
        self.assessments_storage.get_assessment.return_value = mock_assessment

        mock_questions = [
            QuestionDTOFactory(question_id="q1", question_text="Q1 text", difficulty_level=Difficulty.EASY),
            QuestionDTOFactory(question_id="q2", question_text="Q2 text", difficulty_level=Difficulty.MEDIUM),
            QuestionDTOFactory(question_id="q3", question_text="Q3 text", difficulty_level=Difficulty.HARD),
        ]
        self.interactor.get_next_n_questions = MagicMock(return_value=mock_questions)

        expected_attempt = AssessmentAttemptDTO(
            attempt_id="attempt-123",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=0,
            question_ids=[obj.question_id for obj in mock_questions],
            status="START",
            started_at="2025-01-01"
        )
        self.attempt_storage.create_assessment_attempt.return_value = expected_attempt

        # Act
        result = self.interactor.start_assessment_attempt(
            user_id=user_id,
            assessment_id=assessment_id,
            question_selection=Algorithm.RANDOM
        )

        self.user_storage.check_user_exists.assert_called_once_with(user_id=user_id)
        self.assessments_storage.get_assessment.assert_called_once_with(assessment_id=assessment_id)
        self.interactor.get_next_n_questions.assert_called_once()
        self.attempt_storage.create_assessment_attempt.assert_called_once_with(
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=["q1", "q2", "q3"]
        )

        snapshot.assert_match(repr(result), "start_assessment_attempt_success.json")

    def test_start_assessment_attempt_user_not_found(self):
        user_id = "invalid-user"
        assessment_id = "assess-123"

        self.user_storage.check_user_exists.side_effect = UserNotFound(user_id)

        with pytest.raises(UserNotFound):
            self.interactor.start_assessment_attempt(
                user_id=user_id,
                assessment_id=assessment_id,
                question_selection=Algorithm.RANDOM
            )

        self.assessments_storage.get_assessment.assert_not_called()
        self.attempt_storage.create_assessment_attempt.assert_not_called()

    def test_start_assessment_attempt_assessment_not_found(self):
        user_id = "user-001"
        assessment_id = "assessment-1234"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.side_effect = AssessmentIdNotFound(assessment_id)

        with pytest.raises(AssessmentIdNotFound):
            self.interactor.start_assessment_attempt(
                user_id=user_id,
                assessment_id=assessment_id,
                question_selection=Algorithm.FIXED
            )

        self.attempt_storage.create_assessment_attempt.assert_not_called()
