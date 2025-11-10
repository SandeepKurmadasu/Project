import pytest
from unittest.mock import create_autospec

from assessment.exceptions.custom_exceptions import \
    AssessmentIdNotFound
from assessment.interactors.attempts_interactor.start_assessment_attempt_interactor import \
    StartAssessmentAttemptInteractor
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.tests.factories.factories import AssessmentAttemptDTOFactory

from course_management.exceptions.custom_exceptions import \
    UserNotFound
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class TestStartAssessmentAttemptInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.assessments_storage = create_autospec(AssessmentStorageInterface)
        self.validator = create_autospec(AssessmentValidationMixIn)

        self.interactor = StartAssessmentAttemptInteractor(
            attempt_storage=self.attempt_storage,
            user_storage=self.user_storage,
            assessments_storage=self.assessments_storage, )

    def test_start_assessment_attempt_success(self, snapshot):
        # Arrange
        user_id = "user-001"
        assessment_id = "assess-123"

        expected = AssessmentAttemptDTOFactory(
            attempt_id="attempt-456",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=49
        )

        self.attempt_storage.create_assessment_attempt.return_value = expected

        # Act
        result = self.interactor.start_assessment_attempt(user_id,
                                                          assessment_id)

        # Assert

        snapshot.assert_match(repr(result),
                              "start_assessment_attempt_success.json")

    def test_start_assessment_attempt_user_not_found(self, snapshot):
        user_id = "invalid-user"
        assessment_id = "assess-123"

        self.interactor.user_storage.check_user_exists.return_value = False

        with pytest.raises(UserNotFound) as e:
            self.interactor.start_assessment_attempt(user_id, assessment_id)

        self.validator.validate_assessment_exists.assert_not_called()
        self.attempt_storage.create_assessment_attempt.assert_not_called()

        snapshot.assert_match(repr(e.value.user_id), "user_not_found.json")

    def test_start_assessment_attempt_assessment_not_found(self, snapshot):
        user_id = "user-001"
        assessment_id = "assessment-1234"

        self.interactor.assessments_storage.assessment_exists.return_value = False

        with pytest.raises(AssessmentIdNotFound) as e:
            self.interactor.start_assessment_attempt(user_id, assessment_id)

        self.attempt_storage.create_assessment_attempt.assert_not_called()
        snapshot.assert_match(repr(e.value.assessment_id),
                              "assessment_not_found.json")
