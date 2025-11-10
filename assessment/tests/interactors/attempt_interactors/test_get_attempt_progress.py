import pytest
from unittest.mock import create_autospec, patch

from faker import Faker

from assessment.exceptions.custom_exceptions import \
    AttemptIdNotFound
from assessment.interactors.attempts_interactor.get_attempt_progress_interactor import \
    GetAttemptProgressInteractor
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.tests.factories.factories import AssessmentAttemptDTOFactory

Faker.seed(1)


class TestGetAttemptProgressInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.interactor = GetAttemptProgressInteractor(
            assessment_attempt_storage=self.attempt_storage)
        self.attempt_id = "attempt-001"

    def test_get_attempt_progress_success(self, snapshot):
        # Arrange
        expected_dto = AssessmentAttemptDTOFactory(
            attempt_id=self.attempt_id,
            assessment_id="a1",
            user_id="u1",
            total_points=70
        )

        self.attempt_storage.get_assessment_progress.return_value = expected_dto

        # Act
        result = self.interactor.get_attempt_progress(
            attempt_id=self.attempt_id)

        # Assert
        self.attempt_storage.get_assessment_progress.assert_called_once_with(
            attempt_id=self.attempt_id
        )
        snapshot.assert_match(repr(result), "get_attempt_progress_success.txt")

    def test_get_attempt_progress_attempt_not_found(self, snapshot):
        # Arrange
        with patch.object(
                self.interactor,
                "validate_attempt_exists",
                side_effect=AttemptIdNotFound(attempt_id=self.attempt_id)
        ):
            # Act & Assert
            with pytest.raises(AttemptIdNotFound) as e:
                self.interactor.get_attempt_progress(
                    attempt_id=self.attempt_id)

        snapshot.assert_match(repr(e.value.attempt_id),
                              "attempt_id_not_found.txt")
