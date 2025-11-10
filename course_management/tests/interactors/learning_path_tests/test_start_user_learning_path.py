import pytest
from unittest.mock import create_autospec, patch

from faker import Faker

from course_management.exceptions.custom_exceptions import \
    LearningPathIdNotFound
from course_management.interactors.learning_path.start_user_course_learning_path import \
    StartUserCourseLearningPathInteractor
from course_management.interactors.storage_interfaces.learning_path_storage_interface import \
    LearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from course_management.tests.factories.interactor_factories import \
    UserLearningPathDTOFactory

Faker.seed(1)


class TestStartUserCourseLearningPathInteractor:
    def setup_method(self):
        self.learning_path_storage = create_autospec(
            LearningPathStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.user_learning_storage = create_autospec(
            UserLearningPathStorageInterface)

        self.interactor = StartUserCourseLearningPathInteractor(
            learning_path_storage=self.learning_path_storage,
            user_storage=self.user_storage,
            user_learning_storage=self.user_learning_storage,
        )

        self.user_id = "user-101"
        self.learning_path_id = "lp-505"

    def test_start_user_course_learning_path_success(self, snapshot):
        # Arrange
        self.user_storage.check_user_exists.return_value = True
        self.learning_path_storage.learning_path_exist.return_value = True

        mock_course_learning_path = UserLearningPathDTOFactory()
        self.learning_path_storage.get_course_learning_path.return_value = mock_course_learning_path
        self.user_learning_storage.get_user_learning_path_with_id.return_value = None
        self.user_learning_storage.create_user_learning_path.return_value = mock_course_learning_path

        # Act
        result = self.interactor.start_user_course_learning_path(
            user_id=self.user_id, course_learning_path_id=self.learning_path_id
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "start_user_course_learning_path_success.json")

    def test_start_user_course_learning_path_existing_user_path(self,
                                                                snapshot):
        # Arrange
        existing_path = UserLearningPathDTOFactory()
        self.learning_path_storage.learning_path_exist.return_value = True
        self.user_learning_storage.get_user_learning_path_with_id.return_value = existing_path

        # Act
        result = self.interactor.start_user_course_learning_path(
            user_id=self.user_id, course_learning_path_id=self.learning_path_id
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "start_user_course_learning_path_existing.json")

    def test_start_user_course_learning_path_not_found(self, snapshot):
        invalid_learning_path_id = "lp-404"

        with patch(
                "course_management.interactors.learning_path.start_user_course_learning_path.StartUserCourseLearningPathInteractor._validate_learning_path_exists",
                side_effect=LearningPathIdNotFound(
                    learning_path_id=invalid_learning_path_id),
        ):
            with pytest.raises(LearningPathIdNotFound) as exc:
                self.interactor.start_user_course_learning_path(
                    user_id=self.user_id,
                    course_learning_path_id=invalid_learning_path_id,
                )

        snapshot.assert_match(
            repr(exc.value.learning_path_id),
            "learning_path_id_not_found_snapshot.txt",
        )
