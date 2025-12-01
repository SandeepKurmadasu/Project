from datetime import datetime, timezone
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
from course_management.interactors.storage_interfaces.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import TopicStorageInterface
from course_management.tests.interactors.topic_tests.test_for_topics import topic_storage


class TestAttemptAutoEndInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.enrollment_storage = create_autospec(EnrollmentStorageInterface)
        self.topic_storage = create_autospec(TopicStorageInterface)
        self.module_storage = create_autospec(ModuleStorageInterface)
        self.interactor = AttemptAutoEndInteractor(
            attempt_storage=self.attempt_storage,
            assessment_storage=self.assessment_storage,
            enrollment_storage=self.enrollment_storage,
            topic_storage=self.topic_storage,
            module_storage=self.module_storage,
        )

    @freeze_time("2025-11-01 10:30:00")
    def test_auto_end_attempt_when_expired(self, snapshot):
        # Arrange
        started_at = datetime(2025, 11, 1, 9, 0, 0, tzinfo=timezone.utc)  # 1.5 hours earlier
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
                "assessment_id": "assessment-999",
                "estimate_duration_in_mins": 60,  # 1 hour duration
                "attempts_limit": 3,  # Added this line
                "topic_id": "topic_123"
            })()

        # Mock get_user_assessment_attempts
        self.attempt_storage.get_user_assessment_attempts.return_value = [
            AssessmentAttemptDTO(
                attempt_id="attempt-001",
                user_id="user-101",
                assessment_id="assessment-999",
                total_points=50,
                question_ids=[],
                status=StatusEnum.IN_PROGRESS,
                started_at=started_at
            )
        ]

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
        started_at = datetime(2025, 11, 1, 9, 0, 0, tzinfo=timezone.utc)
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
                "assessment_id": "assessment-777",
                "estimate_duration_in_mins": 90,  # 1.5 hours duration
                "attempts_limit": 3,  # Added this line
                "topic_id": "topic_456"
            })()

        # Mock get_user_assessment_attempts
        self.attempt_storage.get_user_assessment_attempts.return_value = [
            AssessmentAttemptDTO(
                attempt_id="attempt-002",
                user_id="user-202",
                assessment_id="assessment-777",
                total_points=40,
                question_ids=[],
                status=StatusEnum.IN_PROGRESS,
                started_at=started_at
            )
        ]

        # Act
        result = self.interactor.auto_end_attempt(attempt_id="attempt-002")

        # Assert
        self.attempt_storage.end_an_attempt.assert_not_called()
        assert result is None