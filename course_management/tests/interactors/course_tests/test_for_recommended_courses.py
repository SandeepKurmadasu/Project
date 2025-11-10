import json
import pytest
from unittest.mock import Mock
from faker import Faker

from course_management.interactors.course.get_recommend_courses import (
    GetRecommendCoursesInteractor,
)
from course_management.interactors.dtos import CourseDTO
from course_management.tests.factories.interactor_factories import (
    CourseDTOFactory,
    EnrollmentDTOFactory,
    UserDTOFactory,
)

Faker.seed(42)


@pytest.fixture(autouse=True)
def set_faker_seed():
    Faker.seed(0)


@pytest.fixture
def course_storage():
    return Mock()


@pytest.fixture
def enrollment_storage():
    return Mock()


@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def interactor(course_storage, enrollment_storage, user_storage):
    return GetRecommendCoursesInteractor(
        course_storage=course_storage,
        enrollment_storage=enrollment_storage,
        user_storage=user_storage,
    )


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CourseDTO):
            return obj.__dict__
        return super().default(obj)


class TestGetRecommended:

    def test_get_recommended_courses_successfully(self, interactor,
                                                  course_storage,
                                                  enrollment_storage,
                                                  user_storage,
                                                  snapshot):
        # Arrange
        user = UserDTOFactory()

        enrolled_courses = [
            EnrollmentDTOFactory(course_id="C001", user_id=user.user_id,
                                 course_percentage=50),
            EnrollmentDTOFactory(course_id="C002", user_id=user.user_id,
                                 course_percentage=80),
        ]

        all_courses = [
            CourseDTOFactory(course_id="C001", title="Course 1"),
            CourseDTOFactory(course_id="C002", title="Course 2"),
            CourseDTOFactory(course_id="C003", title="Course 3"),
            CourseDTOFactory(course_id="C004", title="Course 4"),
        ]

        recommended_courses = [
            CourseDTOFactory(course_id="C003", title="Course 3"),
            CourseDTOFactory(course_id="C004", title="Course 4"),
        ]

        user_storage.check_user_exists.return_value = True
        enrollment_storage.get_user_enrolled_courses.return_value = enrolled_courses
        course_storage.get_all_courses.return_value = all_courses
        course_storage.get_courses.return_value = recommended_courses

        # Act
        result = interactor.get_recommended_courses(user.user_id)

        # Assert
        user_storage.check_user_exists.assert_called_once_with(
            user_id=user.user_id)
        enrollment_storage.get_user_enrolled_courses.assert_called_once_with(
            user_id=user.user_id)
        course_storage.get_courses.assert_called_once()

        assert isinstance(result, list)
        assert all(isinstance(c, CourseDTO) for c in result)
        assert len(result) == 2
        assert result[0].course_id == "C003"

        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], indent=2, sort_keys=True,
                       cls=CustomEncoder),
            "get_recommended_courses_success_snapshot.json"
        )

    def test_user_has_all_courses_enrolled_returns_empty_list(self, interactor,
                                                              course_storage,
                                                              enrollment_storage,
                                                              user_storage,
                                                              snapshot):
        # Arrange
        user = UserDTOFactory()
        enrolled_courses = [
            EnrollmentDTOFactory(course_id="C001", user_id=user.user_id),
            EnrollmentDTOFactory(course_id="C002", user_id=user.user_id),
        ]
        all_courses = [
            CourseDTOFactory(course_id="C001", title="Course 1"),
            CourseDTOFactory(course_id="C002", title="Course 2"),
        ]

        user_storage.check_user_exists.return_value = True
        enrollment_storage.get_user_enrolled_courses.return_value = enrolled_courses
        course_storage.get_all_courses.return_value = all_courses
        course_storage.get_courses.return_value = []  # nothing to recommend

        # Act
        result = interactor.get_recommended_courses(user.user_id)

        # Assert
        assert result == []
        snapshot.assert_match(
            json.dumps(result, indent=2, sort_keys=True),
            "no_recommended_courses_snapshot.json"
        )
