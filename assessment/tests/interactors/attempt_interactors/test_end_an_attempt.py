from datetime import datetime
from unittest.mock import create_autospec, patch

import pytest
from freezegun import freeze_time

from cyber_edu_verse.assessment.exceptions.custom_exceptions import \
    AttemptIdNotFound
from cyber_edu_verse.assessment.interactors.attempts_interactor.end_attempt_interactor import \
    EndAttemptInteractor
from cyber_edu_verse.assessment.interactors.dtos import AssessmentAttemptDTO
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.course_management.interactors.dtos import StatusEnum


class TestEndAttempt:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.interactor = EndAttemptInteractor(
            attempt_storage=self.attempt_storage
        )

    @freeze_time("2024-10-31 10:00:00")
    def test_end_attempt_successfully(self, snapshot):
        self.attempt_storage.end_an_attempt.return_value = AssessmentAttemptDTO(
            attempt_id="attempt-001",
            user_id="user-123",
            assessment_id="assessment-555",
            total_points=100,
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
                "cyber_edu_verse.assessment.interactors.assessment_validations.AssessmentValidationMixIn.validate_attempt_exists"
        ) as mock_validate:
            mock_validate.side_effect = AttemptIdNotFound(attempt_id="attempt-404")

            with pytest.raises(AttemptIdNotFound) as e:
                self.interactor.end_attempt(attempt_id="attempt-404")

            snapshot.assert_match(str(e.value.attempt_id), "end_attempt_not_found_snapshot.json")
