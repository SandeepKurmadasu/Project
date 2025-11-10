import pytest
from unittest.mock import create_autospec

from cyber_edu_verse.assessment.exceptions.custom_exceptions import \
    AttemptIdNotFound
from cyber_edu_verse.assessment.interactors.attempts_interactor.get_attempt_score_interactor import \
    GetAttemptScoreInteractor
from cyber_edu_verse.assessment.interactors.dtos import AttemptScoreDTO
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.assessment.tests.factories.interactor_factories import \
    AssessmentAttemptDTOFactory
from cyber_edu_verse.course_management.interactors.dtos import StatusEnum


class TestGetAttemptScoreInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.interactor = GetAttemptScoreInteractor(
            attempt_storage=self.attempt_storage)

    def test_get_attempt_score_success(self, snapshot):
        # Arrange
        attempt_id = "attempt-123"
        mock_attempt = AssessmentAttemptDTOFactory(
            attempt_id=attempt_id,
            total_points=85,
            user_id="user-111",
            status=StatusEnum.COMPLETE
        )

        self.interactor.validate_attempt_exists_return_value = True
        self.attempt_storage.get_assessment_attempt.return_value = mock_attempt

        expected_dto = AttemptScoreDTO(
            attempt_id=attempt_id,
            user_id="user-111",
            score=85
        )

        # Act
        result = self.interactor.get_attempt_score(attempt_id)

        # Assert

        assert expected_dto == result
        snapshot.assert_match(repr(result), "get_attempt_score_success.txt")

    def test_get_attempt_score_raises_when_not_found(self, snapshot):
        # Arrange
        attempt_id = "attempt_1234"
        self.interactor.attempt_storage.check_attempt_exist.return_value = False

        # Act & Assert
        with pytest.raises(AttemptIdNotFound) as e:
            self.interactor.get_attempt_score(attempt_id)

        self.attempt_storage.get_assessment_attempt.assert_not_called()

        snapshot.assert_match(repr(e.value.attempt_id),
                              "attempt_id_not_found.txt")
