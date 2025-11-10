from unittest.mock import create_autospec, patch

import pytest

from course_management.exceptions.custom_exceptions import \
    UserLearningPathNotFound
from course_management.interactors.dtos import (
    UserLearningPathDTO,
    UserLearningUnitProgressDTO,
    AttemptedTopicStatusEnum,
    StatusEnum
)
from course_management.interactors.learning_path.get_user_learning_path_details import \
    GetUserLearningPathDetailsInteractor
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface


class TestUserCurrentLearningUnitStatus:

    def test_get_user_current_learning_status_success(self, snapshot):
        # Arrange
        user_learning_path_storage = create_autospec(
            UserLearningPathStorageInterface)
        user_learning_units_storage = create_autospec(
            UserLearningUnitStorageInterface)

        interactor = GetUserLearningPathDetailsInteractor(
            user_learning_path_storage=user_learning_path_storage,
            user_learning_unit_storage=user_learning_units_storage
        )

        user_learning_path_id = "ulp-101"
        current_learning_unit_id = "lu-301"

        # Mock: user learning path details
        user_learning_path_storage.get_user_learning_path_with_user_learning_path_id.return_value = UserLearningPathDTO(
            user_learning_path_id=user_learning_path_id,
            user_id="user-10",
            learning_path_id="lp-20",
            current_learning_unit_id=current_learning_unit_id,
            overall_percentage=40,
            status=StatusEnum.IN_PROGRESS
        )

        # Mock: current learning unit progress
        user_learning_units_storage.get_user_learning_unit_progress.return_value = UserLearningUnitProgressDTO(
            learning_unit_id=current_learning_unit_id,
            user_learning_path_id=user_learning_path_id,
            status=AttemptedTopicStatusEnum.COMPLETE,
            percentage=100,
            is_locked=False,
            order=3,
            estimated_duration_in_minutes=45
        )

        # Act
        result = interactor.get_current_learning_unit_status(
            user_learning_path_id)

        # Assert
        snapshot.assert_match(
            repr(result),
            "user_current_learning_unit_status_success_snapshot.json",
        )

    def test_get_user_learning_path_not_found(self, snapshot):
        user_learning_path_storage = create_autospec(
            UserLearningPathStorageInterface)
        user_learning_unit_storage = create_autospec(
            UserLearningUnitStorageInterface)

        interactor = GetUserLearningPathDetailsInteractor(
            user_learning_path_storage=user_learning_path_storage,
            user_learning_unit_storage=user_learning_unit_storage
        )

        invalid_user_learning_path_id = "ulp-404"

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.validate_user_learning_path_exists",
                side_effect=UserLearningPathNotFound(
                    user_learning_path_id=invalid_user_learning_path_id),
        ):
            with pytest.raises(UserLearningPathNotFound) as exc:
                interactor.get_current_learning_unit_status(
                    invalid_user_learning_path_id)

        snapshot.assert_match(
            repr(exc.value),
            "user_learning_path_not_found_snapshots.txt",
        )
