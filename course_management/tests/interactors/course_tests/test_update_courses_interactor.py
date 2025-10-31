import pytest
from unittest.mock import Mock
from faker import Faker
import json
from course_management.interactors.course.update_course_interactor import UpdateCoursesInteractor
from course_management.exceptions.custom_exceptions import (
    DuplicateCourseIdsFound,
    DuplicateTitlesFound,
    UnexpectedLevelTypeFound,
    NotInDBCourseIdsFound,
)
from course_management.tests.factories import UpdateCourseDTOFactory, CourseDTOFactory

def reset_factories():
    Faker.seed(0)
    CourseDTOFactory.reset_sequence(0)
    UpdateCourseDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def storage():
    s = Mock()
    s.get_valid_course_ids.return_value = []  # NO VALID COURSE IDS
    return s


@pytest.fixture
def interactor(storage):
    return UpdateCoursesInteractor(course_storage=storage)


def test_update_courses_successfully(interactor, storage,snapshot):
    #Arrange
    input_courses = UpdateCourseDTOFactory.build_batch(2)
    expected = [
        CourseDTOFactory(
            course_id=input_courses[0].course_id,
            title=input_courses[0].title,
            description=input_courses[0].description,
            category=input_courses[0].category,
            level=input_courses[0].level,
            average_rating=0,
            estimated_duration=120,
        ),
        CourseDTOFactory(
            course_id=input_courses[1].course_id,
            title=input_courses[1].title,
            description=input_courses[1].description,
            category=input_courses[1].category,
            level=input_courses[1].level,
            average_rating=0,
            estimated_duration=120,
        ),
    ]
    storage.get_valid_course_ids.return_value = [c.course_id for c in input_courses]  # Mock valid IDs
    storage.update_courses.return_value = expected

    # Act
    result = interactor.update_courses(input_courses)

    # Assert
    assert len(result) == 2
    assert result[0].course_id == input_courses[0].course_id
    assert result[0].title == input_courses[0].title
    storage.update_courses.assert_called_once_with(courses=input_courses)

    #snapshot
    snapshot.assert_match(
        result,
        "update_courses_snapshot.json"
    )


def test_duplicate_course_ids_raises(interactor,snapshot):
    # Arrange
    course_id = "C0001"
    courses = [UpdateCourseDTOFactory.build(course_id=course_id), UpdateCourseDTOFactory.build(course_id=course_id)]

    # Act
    with pytest.raises(DuplicateCourseIdsFound) as exc:
        interactor.update_courses(courses)

    # Assert
    assert exc.value.course_ids == [course_id]

    #snapshot
    snapshot.assert_match(
        exc.value.course_ids,
        "duplicate_course_ids_snapshot.json"
    )


def test_duplicate_titles_raises(interactor,snapshot):
    # Arrange
    title = "Python 101"
    courses = [UpdateCourseDTOFactory.build(title=title), UpdateCourseDTOFactory.build(title=title)]

    # Act
    with pytest.raises(DuplicateTitlesFound) as exc:
        interactor.update_courses(courses)

    # Assert
    assert exc.value.titles == [title]

    #snapshot
    snapshot.assert_match(
        exc.value.titles,
        "duplicate_titles_snapshot.json"
    )


@pytest.mark.parametrize("bad_level", ["pro", "expert", "", None])
def test_invalid_level_raises(interactor, bad_level,snapshot):
    # Arrange
    course = UpdateCourseDTOFactory.build(level=bad_level)

    # Act
    with pytest.raises(UnexpectedLevelTypeFound) as exc:
        interactor.update_courses([course])

    # Assert
    assert bad_level in exc.value.level_types

    #snapshot
    snapshot.assert_match(
        exc.value.level_types,
        f"invalid_level_{bad_level}_snapshot.json"
    )


def test_course_ids_not_in_db_raises(interactor, storage,snapshot):
    # Arrange
    course = UpdateCourseDTOFactory.build(course_id="C9999")
    storage.get_valid_course_ids.return_value = ["C0001"]

    # Act
    with pytest.raises(NotInDBCourseIdsFound) as exc:
        interactor.update_courses([course])

    # Assert
    assert exc.value.course_ids == ["C9999"]

    #snapshot
    snapshot.assert_match(
        exc.value.course_ids,
        "not_in_db_course_ids_snapshot.json"
    )