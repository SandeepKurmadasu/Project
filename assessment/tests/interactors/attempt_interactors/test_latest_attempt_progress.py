import pytest
from unittest.mock import create_autospec

from faker import Faker

from assessment.exceptions.custom_exceptions import \
    AssessmentIdNotFound
from assessment.interactors.attempts_interactor.get_latest_attempt_interactor import \
    GetLatestAssessmentAttemptInteractor
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.tests.factories.factories import AssessmentAttemptDTOFactory

Faker.seed(1)


class TestGetLatestAssessmentAttemptInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.interactor = GetLatestAssessmentAttemptInteractor(
            attempt_storage=self.attempt_storage,
            assessments_storage=self.assessment_storage
        )

    def test_get_latest_assessment_attempt_success(self, snapshot):
        # Arrange
        user_id = "user-123"
        assessment_id = "assessment-456"
        question_ids = ["Q1", "Q2", "Q3"]
        mock_attempt = AssessmentAttemptDTOFactory(
            attempt_id="attempt-001",
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=question_ids,
            total_points=50
        )

        # validations
        self.interactor.validate_assessment_exists.return_value = True
        self.attempt_storage.get_latest_assessment_attempt.return_value = mock_attempt

        # Act
        result = self.interactor.get_latest_assessment_attempt(
            user_id=user_id, assessment_id=assessment_id
        )

        # Assert
        self.interactor.validate_assessment_exists(assessment_id,
                                                   self.assessment_storage)
        self.attempt_storage.get_latest_assessment_attempt.assert_called_once_with(
            user_id=user_id, assessment_id=assessment_id
        )

        # Snapshot test
        snapshot.assert_match(repr(result),
                              "latest_assessment_attempt_dto.json")

    def test_get_latest_assessment_attempt_assessment_not_found(self,
                                                                snapshot):
        # Arrange
        user_id = "user-123"
        assessment_id = "invalid-assessment"

        self.interactor.assessments_storage.assessment_exists.return_value = False

        # Act & Assert
        with pytest.raises(AssessmentIdNotFound) as e:
            self.interactor.get_latest_assessment_attempt(user_id=user_id,
                                                          assessment_id=assessment_id)

        self.attempt_storage.get_latest_assessment_attempt.assert_not_called()

        snapshot.assert_match(repr(e.value.assessment_id),
                              "assessment_id_not_found.txt")
