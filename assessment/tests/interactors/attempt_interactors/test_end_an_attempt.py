from datetime import datetime
from unittest.mock import create_autospec, patch

import pytest
from freezegun import freeze_time

from assessment.exceptions.custom_exceptions import \
    AttemptIdNotFound
from assessment.interactors.attempts_interactor.end_attempt_interactor import \
    EndAttemptInteractor
from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import AssessmentStorageInterface
from course_management.interactors.dtos import StatusEnum


class TestEndAttempt:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.enrollment_storage = create_autospec(AttemptStorageInterface)
        self.interactor = EndAttemptInteractor(
            attempt_storage=self.attempt_storage,
            assessment_storage=self.assessment_storage,
            enrollment_storage=self.enrollment_storage
        )


    @freeze_time("2024-10-31 10:00:00")
    def test_end_attempt_successfully(self, snapshot):
        self.attempt_storage.end_an_attempt.return_value = AssessmentAttemptDTO(
            attempt_id="attempt-001",
            user_id="user-123",
            assessment_id="assessment-555",
            total_points=100,
            question_ids=[],
            status=StatusEnum.COMPLETE,
            started_at=datetime(2025, 10, 31, 10, 0, 0)
        )

        result = self.interactor.end_attempt(attempt_id="attempt-001")

        self.attempt_storage.end_an_attempt.assert_called_once_with(
            attempt_id="attempt-001",
            status=StatusEnum.COMPLETE
        )

        snapshot.assert_match(repr(result),
                              "end_attempt_success_snapshot.json")

    def test_end_attempt_raises_exception_when_attempt_not_found(self,
                                                                 snapshot):
        with patch(
                "assessment.interactors.common_validation_mixin.AssessmentValidationMixIn.validate_attempt_exists"
        ) as mock_validate:
            mock_validate.side_effect = AttemptIdNotFound(
                attempt_id="attempt-404")

            with pytest.raises(AttemptIdNotFound) as e:
                self.interactor.end_attempt(attempt_id="attempt-404")

            snapshot.assert_match(str(e.value.attempt_id),
                                  "end_attempt_not_found_snapshot.json")
