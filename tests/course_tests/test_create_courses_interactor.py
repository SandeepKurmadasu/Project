import pytest
from unittest.mock import Mock
from faker import Faker
import json
Faker.seed(42)

from course_management.interactors.course.create_course_interactor import CreateCoursesInteractor
from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    UnexpectedLevelTypeFound,
    DuplicateCourseTitleFound,
)

from tests.factories import CreateCourseDTOFactory, CourseDTOFactory

@pytest.fixture(autouse=True)
def reset_factories():
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
            course_id="C0001",
            title=input_courses[0].title,
            description=input_courses[0].description,
            category=input_courses[0].category,
            level=input_courses[0].level,
            average_rating=0,
        ),
        CourseDTOFactory(
            course_id="C0002",
            title=input_courses[1].title,
            description=input_courses[1].description,
            category=input_courses[1].category,
            level=input_courses[1].level,
            average_rating=0,
        ),
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
        json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
        "create_courses_snapshot.json"
    )


def test_duplicate_titles_raises(interactor, snapshot):
    # RESET SEQUENCES
    CreateCourseDTOFactory.reset_sequence(0)

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
        json.dumps(exc.value.titles, sort_keys=True, indent=2),
        "duplicate_titles_snapshot.json"
    )


@pytest.mark.parametrize("bad_level", ["pro", "expert", "", None])
def test_invalid_level_raises(interactor, bad_level, snapshot):
    # RESET SEQUENCES
    CreateCourseDTOFactory.reset_sequence(0)

    # ARRANGE
    course = CreateCourseDTOFactory.build(level=bad_level)

    # ACT
    with pytest.raises(UnexpectedLevelTypeFound) as exc:
        interactor.create_courses([course])

    # ASSERT
    assert bad_level in exc.value.level_types

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps(exc.value.level_types, sort_keys=True, indent=2),
        f"invalid_level_{bad_level}_snapshot.json"
    )


def test_title_already_exists_raises(interactor, storage, snapshot):
    # RESET SEQUENCES
    CreateCourseDTOFactory.reset_sequence(0)

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
        json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
        "existing_title_snapshot.json"
    )
