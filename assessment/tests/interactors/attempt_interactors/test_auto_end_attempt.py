from datetime import datetime
from unittest.mock import create_autospec

from freezegun import freeze_time

from assessment.interactors.attempts_interactor.auto_end_attempt_interactor import \
    AttemptAutoEndInteractor
from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.dtos import StatusEnum


class TestAttemptAutoEndInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.interactor = AttemptAutoEndInteractor(
            attempt_storage=self.attempt_storage,
            assessment_storage=self.assessment_storage
        )

    @freeze_time("2025-11-01 10:30:00")
    def test_auto_end_attempt_when_expired(self, snapshot):
        # Arrange
        started_at = datetime(2025, 11, 1, 9, 0, 0)  # 1.5 hours earlier
        self.attempt_storage.get_assessment_attempt.return_value = AssessmentAttemptDTO(
            attempt_id="attempt-001",
            user_id="user-101",
            assessment_id="assessment-999",
            total_points=50,
            question_ids=[],
            status=StatusEnum.IN_PROGRESS,
            started_at=started_at
        )

        self.assessment_storage.get_assessment.return_value = type(
            "Assessment", (), {
                "estimate_duration_in_mins": 60  # 1 hour duration
            })()

        expected_result = AssessmentAttemptDTO(
            attempt_id="attempt-001",
            user_id="user-101",
            assessment_id="assessment-999",
            total_points=50,
            question_ids=[],
            status=StatusEnum.COMPLETE,
            started_at=started_at
        )
        self.attempt_storage.end_an_attempt.return_value = expected_result

        # Act
        result = self.interactor.auto_end_attempt(attempt_id="attempt-001")

        # Assert
        self.attempt_storage.end_an_attempt.assert_called_once_with(
            attempt_id="attempt-001",
            status=StatusEnum.COMPLETE
        )
        snapshot.assert_match(repr(result),
                              "auto_end_attempt_success_snapshot.json")

    @freeze_time("2025-11-01 09:30:00")
    def test_auto_end_attempt_not_expired(self):
        started_at = datetime(2025, 11, 1, 9, 0, 0)
        self.attempt_storage.get_assessment_attempt.return_value = AssessmentAttemptDTO(
            attempt_id="attempt-002",
            user_id="user-202",
            assessment_id="assessment-777",
            total_points=40,
            question_ids=[],
            status=StatusEnum.IN_PROGRESS,
            started_at=started_at
        )

        self.assessment_storage.get_assessment.return_value = type(
            "Assessment", (), {
                "estimate_duration_in_mins": 90  # 1.5 hours duration
            })()

        # Act
        result = self.interactor.auto_end_attempt(attempt_id="attempt-002")

        # Assert
        self.attempt_storage.end_an_attempt.assert_not_called()
        assert result is None

    # def test_attempt_not_found(self,snapshot):
