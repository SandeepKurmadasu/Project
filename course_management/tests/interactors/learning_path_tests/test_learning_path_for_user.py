import pytest
from unittest.mock import MagicMock, patch

from faker import Faker

from course_management.exceptions.custom_exceptions import \
    UserLearningPathNotFound
from course_management.interactors.learning_path.get_user_learning_path_details import \
    GetUserLearningPathDetailsInteractor
from course_management.tests.factories.interactor_factories import \
    UserLearningPathDTOFactory

Faker.seed(1)


class TestUserLearningPath:

    @pytest.mark.usefixtures("snapshot")
    def test_get_user_learning_path_success(self, snapshot):
        # Arrange
        user_learning_path_storage = MagicMock()
        user_learning_unit_storage = MagicMock()

        interactor = GetUserLearningPathDetailsInteractor(
            user_learning_path_storage=user_learning_path_storage,
            user_learning_unit_storage=user_learning_unit_storage)

        user_learning_path_id = "ulp-123"

        user_learning_path = UserLearningPathDTOFactory(
            user_learning_path_id=user_learning_path_id)

        user_learning_path_storage.get_user_learning_path_with_user_learning_path_id.return_value = user_learning_path

        # Act
        result = interactor.get_user_learning_path(
            user_learning_path_id=user_learning_path_id)

        snapshot.assert_match(
            repr(result),
            "get_user_learning_path_success_snapshot.txt",
        )

    def test_get_user_learning_path_not_found(self, snapshot):
        user_learning_path_storage = patch(
            "course_management.interactors.learning_path.get_user_learning_path_details.GetUserLearningPathDetailsInteractor"
        ).start()
        user_learning_unit_storage = MagicMock()

        interactor = GetUserLearningPathDetailsInteractor(
            user_learning_path_storage=user_learning_path_storage,
            user_learning_unit_storage=user_learning_unit_storage)

        invalid_user_learning_path_id = "ulp-404"

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.validate_user_learning_path_exists",
                side_effect=UserLearningPathNotFound(
                    user_learning_path_id=invalid_user_learning_path_id),
        ):
            with pytest.raises(UserLearningPathNotFound) as exc:
                interactor.get_user_learning_path(
                    invalid_user_learning_path_id)

        snapshot.assert_match(
            repr(exc.value),
            "user_learning_path_not_found_snapshots.txt",
        )
