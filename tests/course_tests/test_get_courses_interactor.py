import pytest
from unittest.mock import Mock

from course_management.interactors.course.get_courses_interactor import GetCoursesInteractor
from course_management.exceptions.custom_exceptions import (
    DuplicateCourseIdsFound,
    NotInDBCourseIdsFound,
)
from tests.factories import CourseDTOFactory


@pytest.fixture
def storage():
    s = Mock()
    s.get_valid_course_ids.return_value = []  # NO VALID COURSE ID'S
    return s


@pytest.fixture
def interactor(storage):
    return GetCoursesInteractor(course_storage=storage)


# --- Success Case ---
def test_get_courses_successfully(interactor, storage):
    # Arrange
    course_ids = ["C0001", "C0002"]
    expected = [
        CourseDTOFactory(course_id="C0001", title="Course-1", average_rating=0, estimated_duration=120),
        CourseDTOFactory(course_id="C0002", title="Course-2", average_rating=0, estimated_duration=120),
    ]
    storage.get_valid_course_ids.return_value = course_ids
    storage.get_courses.return_value = expected

    # Act
    result = interactor.get_courses(course_ids)

    # Assert
    assert len(result) == 2
    assert result[0].course_id == "C0001"
    assert result[0].title == "Course-1"
    storage.get_courses.assert_called_once_with(course_ids=course_ids)



def test_duplicate_course_ids_raises(interactor):
    # Arrange
    course_ids = ["C0001", "C0001"]

    # Act
    with pytest.raises(DuplicateCourseIdsFound) as exc:
        interactor.get_courses(course_ids)

    # Assert
    assert exc.value.course_ids == ["C0001"]


def test_course_ids_not_in_db_raises(interactor, storage):
    # Arrange
    course_ids = ["C9999"]
    storage.get_valid_course_ids.return_value = ["C0001"]

    # Act
    with pytest.raises(NotInDBCourseIdsFound) as exc:
        interactor.get_courses(course_ids)

    # Assert
    assert exc.value.course_ids == ["C9999"]