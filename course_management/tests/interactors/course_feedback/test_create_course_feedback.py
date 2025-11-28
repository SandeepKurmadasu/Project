import json

import pytest
from unittest.mock import Mock
from faker import Faker

from course_management.interactors.feedback.create_course_feedback_interactor import (
    CreateCourseFeedbackInteractor,
)
from course_management.interactors.dtos import CourseFeedbackDTO, CourseDTO, \
    CourseCategoryEnum, LevelEnum
from course_management.exceptions.custom_exceptions import (
    UserNotFound,
    CourseNotFound,
)

faker = Faker()
Faker.seed(10)


@pytest.fixture
def course_storage():
    return Mock()


@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def feedback_storage():
    return Mock()


@pytest.fixture
def interactor(course_storage, user_storage, feedback_storage):
    return CreateCourseFeedbackInteractor(
        feedback_storage=feedback_storage,
        course_storage=course_storage,
        user_storage=user_storage,
    )


@pytest.mark.django_db
class TestCreateCourseFeedback:

    def test_create_feedback_success(self, interactor,
                                     course_storage,
                                     user_storage,
                                     feedback_storage,
                                     snapshot):
        # ARRANGE
        feedback_input = CourseFeedbackDTO(
            course_id="C001",
            user_id="U001",
            rating=4,
            message="Nice course"
        )

        course_storage.check_course_exists.return_value = True
        user_storage.check_user_exists.return_value = True

        feedback_storage.create_course_feedback.return_value = feedback_input

        feedback_storage.get_course_rating.return_value = [
            Mock(rating=4),
            Mock(rating=5),
        ]

        course_storage.update_course_rating.return_value = CourseDTO(
            course_id="C001",
            title="Python",
            description="Basic Python",
            category=CourseCategoryEnum.DEVELOPMENT,
            level=LevelEnum.BEGINNER,
            average_rating=4.5,
            estimated_duration=10,
        )

        # ACT
        result = interactor.create_course_feedback(feedback_input)

        # ASSERT
        snapshot.assert_match(
            repr(result),
            "create_feedback_success_snapshot.json",
        )

    def test_course_not_found(self, interactor, course_storage, snapshot):
        # ARRANGE
        feedback = CourseFeedbackDTO(
            course_id="C404",
            user_id="U001",
            rating=5,
            message="good"
        )

        course_storage.check_course_exists.return_value = False

        # ASSERT
        with pytest.raises(CourseNotFound) as exc:
            interactor.create_course_feedback(feedback)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "course_not_found_snapshot.json",
        )

    def test_user_not_found(self, interactor, user_storage, snapshot):
        # ARRANGE
        feedback = CourseFeedbackDTO(
            course_id="C001",
            user_id="U404",
            rating=5,
            message="good"
        )

        user_storage.check_user_exists.return_value = False

        # ASSERT
        with pytest.raises(UserNotFound) as exc:
            interactor.create_course_feedback(feedback)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "user_not_found_snapshot.json",
        )

    def test_rating_updates_correctly(self, interactor,
                                      course_storage,
                                      user_storage,
                                      feedback_storage,
                                      snapshot):
        # ARRANGE
        feedback = CourseFeedbackDTO(
            course_id="C010",
            user_id="U010",
            rating=3,
            message="good"
        )

        course_storage.check_course_exists.return_value = True
        user_storage.check_user_exists.return_value = True

        feedback_storage.create_course_feedback.return_value = feedback

        feedback_storage.get_course_rating.return_value = [
            Mock(rating=3),
            Mock(rating=4),
            Mock(rating=5),
        ]

        # ACT
        interactor.create_course_feedback(feedback)

        # ASSERT
        course_storage.update_course_rating.assert_called_once_with(
            course_id="C010",
            rating=4.0,
        )

        snapshot.assert_match(
            json.dumps({"expected_rating": 4.0}, indent=2),
            "rating_update_snapshot.json",
        )
