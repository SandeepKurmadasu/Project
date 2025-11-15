import pytest
from unittest.mock import create_autospec

from types import SimpleNamespace
from faker import Faker

from course_management.exceptions.custom_exceptions import LearningPathIdNotFound
from course_management.interactors.learning_path.start_user_course_learning_path import (
    StartUserCourseLearningPathInteractor,
)
from course_management.interactors.storage_interfaces.learning_path_storage_interface import (
    LearningPathStorageInterface,
)
from course_management.interactors.storage_interfaces.user_learning_path import (
    UserLearningPathStorageInterface,
)
from course_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import (
    LearningUnitStorageInterface,
)
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import (
    UserLearningUnitStorageInterface,
)
from course_management.interactors.dtos import CreateUserLearningUnit
from course_management.tests.factories.interactor_factories import (
    UserLearningPathDTOFactory,
)

Faker.seed(1)


class TestStartUserCourseLearningPathInteractor:
    def setup_method(self):
        self.learning_path_storage = create_autospec(LearningPathStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.user_learning_storage = create_autospec(UserLearningPathStorageInterface)
        self.learning_unit_storage = create_autospec(LearningUnitStorageInterface)
        self.user_learning_unit_storage = create_autospec(
            UserLearningUnitStorageInterface
        )

        self.interactor = StartUserCourseLearningPathInteractor(
            learning_path_storage=self.learning_path_storage,
            user_storage=self.user_storage,
            user_learning_storage=self.user_learning_storage,
            learning_unit_storage=self.learning_unit_storage,
            user_learning_unit_storage=self.user_learning_unit_storage,
        )

        self.user_id = "user-101"
        self.learning_path_id = "lp-505"

    def test_start_user_course_learning_path_success(self, snapshot):
        # Arrange
        self.user_storage.check_user_exists.return_value = True
        self.learning_path_storage.learning_path_exist.return_value = True

        mock_user_learning_path = UserLearningPathDTOFactory()

        learning_units = [
            SimpleNamespace(learning_unit_id="lu-1"),
            SimpleNamespace(learning_unit_id="lu-2"),
        ]

        self.learning_unit_storage.get_learning_units_by_learning_path_id.return_value = (
            learning_units
        )
        self.user_learning_storage.get_user_learning_path_with_id.return_value = None
        self.user_learning_storage.create_user_learning_path.return_value = (
            mock_user_learning_path
        )

        # Act
        result = self.interactor.start_user_course_learning_path(
            user_id=self.user_id,
            course_learning_path_id=self.learning_path_id,
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "start_user_course_learning_path_success.json",
        )

        # Assert
        self.user_learning_unit_storage.create_user_learning_units.assert_called_once()
        (create_input,), _ = (
            self.user_learning_unit_storage.create_user_learning_units.call_args
        )

        assert len(create_input) == len(learning_units)
        assert all(
            isinstance(dto, CreateUserLearningUnit) for dto in create_input
        ), "Interactor should pass CreateUserLearningUnit DTOs to storage"

        created_ids = {dto.learning_unit_id for dto in create_input}
        assert created_ids == {"lu-1", "lu-2"}
        assert all(
            dto.user_learning_path_id == mock_user_learning_path.user_learning_path_id
            for dto in create_input
        )

    def test_start_user_course_learning_path_existing_user_path(self, snapshot):
        # Arrange
        self.user_storage.check_user_exists.return_value = True
        self.learning_path_storage.learning_path_exist.return_value = True

        existing_path = UserLearningPathDTOFactory()
        self.user_learning_storage.get_user_learning_path_with_id.return_value = (
            existing_path
        )

        # Act
        result = self.interactor.start_user_course_learning_path(
            user_id=self.user_id,
            course_learning_path_id=self.learning_path_id,
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "start_user_course_learning_path_existing.json",
        )

    def test_start_user_course_learning_path_not_found(self, snapshot):
        # Arrange
        self.user_storage.check_user_exists.return_value = True
        self.learning_path_storage.learning_path_exist.return_value = False

        invalid_learning_path_id = "lp-404"

        # Act & Assert
        with pytest.raises(LearningPathIdNotFound) as exc:
            self.interactor.start_user_course_learning_path(
                user_id=self.user_id,
                course_learning_path_id=invalid_learning_path_id,
            )

        snapshot.assert_match(
            repr(exc.value.learning_path_id),
            "learning_path_id_not_found_snapshot.txt",
        )

