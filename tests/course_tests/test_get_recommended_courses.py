# tests/test_get_recommend_courses_interactor.py
import pytest
from unittest.mock import Mock

from course_management.interactors.course.get_recommended_courses  import GetRecommendCoursesInteractor
from course_management.exceptions.custom_exceptions import InvalidUserIdError
from tests.factories import CourseDTOFactory, EnrollmentDTOFactory


@pytest.fixture
def course_storage():
    s = Mock()
    s.get_all_course_ids.return_value = []
    s.get_recommend_courses.return_value = []
    return s


@pytest.fixture
def enrollment_storage():
    s = Mock()
    s.get_user_enrolled_courses.return_value = []
    return s


@pytest.fixture
def interactor(course_storage, enrollment_storage):
    return GetRecommendCoursesInteractor(course_storage=course_storage, enrollment_storage=enrollment_storage)


def test_get_recommended_courses_successfully(interactor, course_storage, enrollment_storage):
    # Arrange
    user_id = "user123"
    enrolled_courses = [
        EnrollmentDTOFactory(id=1, user_id=user_id, course_id="C0001", course_percentage=50),
        EnrollmentDTOFactory(id=2, user_id=user_id, course_id="C0002", course_percentage=75),
    ]
    all_course_ids = ["C0001", "C0002", "C0003", "C0004"]
    recommended_courses = [
        CourseDTOFactory(course_id="C0003", title="Course-3"),
        CourseDTOFactory(course_id="C0004", title="Course-4"),
    ]
    enrollment_storage.get_user_enrolled_courses.return_value = [e.course_id for e in enrolled_courses]
    course_storage.get_all_course_ids.return_value = all_course_ids
    course_storage.get_recommend_courses.return_value = recommended_courses

    # Act
    result = interactor.get_recommended_courses(user_id)

    # Assert
    assert len(result) == 2
    assert result[0].course_id == "C0003"
    assert result[1].course_id == "C0004"
    course_storage.get_recommend_courses.assert_called_once_with(course_ids=["C0003", "C0004"])


@pytest.mark.parametrize("invalid_user_id", [None, ""])
def test_invalid_user_id_raises(interactor, invalid_user_id):
    # Act
    with pytest.raises(InvalidUserIdError) as exc:
        interactor.get_recommended_courses(invalid_user_id)

    # Assert
    assert str(exc.value) == "User ID must be a non-empty string"