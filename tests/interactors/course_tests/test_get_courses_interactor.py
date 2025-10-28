import json
import pytest
from unittest.mock import Mock
from faker import Faker
Faker.seed(42)
from course_management.interactors.course.get_courses_interactor import GetCoursesInteractor
from course_management.exceptions.custom_exceptions import (
    DuplicateCourseIdsFound,
    NotInDBCourseIdsFound,
)
from tests.factories import CourseDTOFactory

@pytest.fixture(autouse=True)
def reset_factories():
    CourseDTOFactory.reset_sequence(0)
    yield

@pytest.fixture
def storage():
    s = Mock()
    s.get_valid_course_ids.return_value = []
    yield s
    s.reset_mock()


@pytest.fixture
def interactor(storage):
    return GetCoursesInteractor(course_storage=storage)


def test_get_courses_successfully(interactor, storage,snapshot):
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

    #snapshot
    snapshot.assert_match(
        json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
        "get_courses_snapshot.json"
    )



def test_duplicate_course_ids_raises(interactor,snapshot):
    # Arrange
    course_ids = ["C0001", "C0001"]

    # Act
    with pytest.raises(DuplicateCourseIdsFound) as exc:
        interactor.get_courses(course_ids)

    # Assert
    assert exc.value.course_ids == ["C0001"]

    #snapshot
    snapshot.assert_match(
        json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
        "duplicate_course_ids_snapshot.json"
    )


def test_course_ids_not_in_db_raises(interactor, storage,snapshot):
    # Arrange
    course_ids = ["C9999"]
    storage.get_valid_course_ids.return_value = ["C0001"]

    # Act
    with pytest.raises(NotInDBCourseIdsFound) as exc:
        interactor.get_courses(course_ids)

    # Assert
    assert exc.value.course_ids == ["C9999"]

    #snapshot
    snapshot.assert_match(
        json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
        "not_in_db_course_ids_snapshot.json"
    )