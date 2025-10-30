import pytest
from unittest.mock import Mock
from faker import Faker

Faker.seed(42)

from course_management.interactors.course.create_courses_interactor import CreateCoursesInteractor
from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    UnexpectedLevelTypeFound,
    DuplicateCourseTitleFound,
)

from course_management.tests.factories import CreateCourseDTOFactory, CourseDTOFactory

@pytest.fixture(autouse=True)
def reset_factories():
    Faker.seed(0)
    CourseDTOFactory.reset_sequence(0)
    CreateCourseDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def storage():
    s = Mock()
    s.get_title_course_ids.return_value = []
    yield s
    s.reset_mock()


@pytest.fixture
def interactor(storage):
    return CreateCoursesInteractor(course_storage=storage)


def test_create_courses_successfully(interactor, storage, snapshot):

    # ARRANGE
    input_courses = CreateCourseDTOFactory.build_batch(2)
    expected = [
        CourseDTOFactory(
            course_id="C0002",
            title=course.title,
            description=input_courses[1].description,
            category=input_courses[1].category,
            level=input_courses[1].level,
            average_rating=0,
        )
        for course in input_courses
    ]
    storage.create_courses.return_value = expected

    # ACT
    result = interactor.create_courses(input_courses)

    # ASSERT
    assert len(result) == 2
    assert result[0].course_id == "C0001"
    assert result[0].title == input_courses[0].title
    storage.create_courses.assert_called_once_with(courses=input_courses)

    # SNAPSHOT
    snapshot.assert_match(
        result,
        "create_courses_snapshot.json"
    )


def test_duplicate_titles_raises(interactor, snapshot):
    # ARRANGE
    title = "Python 101"
    courses = [CreateCourseDTOFactory.build(title=title), CreateCourseDTOFactory.build(title=title)]

    # ACT
    with pytest.raises(DuplicateTitlesFound) as exc:
        interactor.create_courses(courses)

    # ASSERT
    assert exc.value.titles == [title]

    # SNAPSHOT
    snapshot.assert_match(
        exc.value.titles,
        "duplicate_titles_snapshot.json"
    )


@pytest.mark.parametrize("bad_level", ["pro", "expert", "", None])
def test_invalid_level_raises(interactor, bad_level, snapshot):
    # ARRANGE
    course = CreateCourseDTOFactory.build(level=bad_level)

    # ACT
    with pytest.raises(UnexpectedLevelTypeFound) as exc:
        interactor.create_courses([course])

    # ASSERT
    assert bad_level in exc.value.level_types

    # SNAPSHOT
    snapshot.assert_match(
        exc.value.level_types,
        f"invalid_level_{bad_level}_snapshot.json"
    )


def test_title_already_exists_raises(interactor, storage, snapshot):
    # ARRANGE
    storage.get_title_course_ids.return_value = ["C9999"]
    course = CreateCourseDTOFactory.build(title="Django Pro")

    # ACT
    with pytest.raises(DuplicateCourseTitleFound) as exc:
        interactor.create_courses([course])

    # ASSERT
    assert exc.value.course_ids == ["C9999"]

    # SNAPSHOT
    snapshot.assert_match(
        exc.value.course_ids,
        "existing_title_snapshot.json"
    )
