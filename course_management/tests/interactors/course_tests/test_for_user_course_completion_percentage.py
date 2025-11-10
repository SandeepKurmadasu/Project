import json
import pytest
from unittest.mock import Mock
from faker import Faker

from course_management.interactors.course.get_user_course_completion_percentage import (
    GetUserCourseCompletionPercentageInteractor,
)
from course_management.exceptions.custom_exceptions import \
    UserNotEnrolledCourse


@pytest.fixture(autouse=True)
def set_faker_seed():
    Faker.seed(1)


@pytest.fixture
def course_storage():
    return Mock()


@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def enrollment_storage():
    return Mock()


@pytest.fixture
def user_learning_path_storage():
    return Mock()


@pytest.fixture
def interactor(course_storage, user_storage, enrollment_storage,
               user_learning_path_storage):
    return GetUserCourseCompletionPercentageInteractor(
        enrollment_storage=enrollment_storage,
        user_storage=user_storage,
        course_storage=course_storage,
        user_learning_path_storage=user_learning_path_storage,
    )


class TestGetUserCourseCompletionPercentage:
    def test_get_user_course_completion_percentage_success(self, interactor,
                                                           snapshot):
        # Arrange
        user_id = "U001"
        course_id = "C001"

        interactor.user_storage.check_user_exists.return_value = None
        interactor.course_storage.check_course_exists.return_value = None
        interactor.enrollment_storage.check_user_course_enrollment_exist.return_value = True

        mock_learning_progress = Mock(overall_percentage=85)
        interactor.user_learning_path_storage.get_user_learning_path.return_value = mock_learning_progress

        # Act
        result = interactor.get_user_course_completion_percentage(
            course_id=course_id,
            user_id=user_id)

        # Assert
        interactor.enrollment_storage.update_course_percentage.assert_called_once_with(
            user_id=user_id, course_id=course_id, percentage=85
        )

        snapshot.assert_match(
            repr(result),
            "get_user_course_completion_percentage_success.json",
        )

    def test_get_user_course_completion_percentage_user_not_enrolled(self,
                                                                     interactor,
                                                                     snapshot):
        # Arrange
        user_id = "U002"
        course_id = "C002"

        interactor.user_storage.check_user_exists.return_value = None
        interactor.course_storage.check_course_exists.return_value = None
        interactor.enrollment_storage.check_user_course_enrollment_exist.return_value = False

        # Act + Assert
        with pytest.raises(UserNotEnrolledCourse) as e:
            interactor.get_user_course_completion_percentage(
                course_id=course_id,
                user_id=user_id)

        assert str(e.value) == user_id

        snapshot.assert_match(
            repr(e.value.user_id),
            "user_not_enrolled_course_error.json",
        )

    def test_calls_all_validation_methods(self, interactor):
        # Arrange
        user_id = "U123"
        course_id = "C999"

        interactor.user_storage.check_user_exists.return_value = None
        interactor.course_storage.check_course_exists.return_value = None
        interactor.enrollment_storage.check_user_course_enrollment_exist.return_value = True

        interactor.user_learning_path_storage.get_user_learning_path.return_value = Mock(
            overall_percentage=75)

        # Act
        interactor.get_user_course_completion_percentage(course_id=course_id,
                                                         user_id=user_id)

        # Assert validation calls
        interactor.user_storage.check_user_exists.assert_called_once_with(
            user_id=user_id)
        interactor.course_storage.check_course_exists.assert_called_once_with(
            course_id=course_id)
        interactor.enrollment_storage.check_user_course_enrollment_exist.assert_called_once_with(
            user_id=user_id, course_id=course_id
        )
