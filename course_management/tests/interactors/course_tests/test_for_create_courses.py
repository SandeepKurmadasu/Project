import json
import pytest
from unittest.mock import Mock
from faker import Faker

from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    UnexpectedLevelTypeFound,
    DuplicateCourseTitleFound,
)
from course_management.interactors.course.create_course_interactor import (
    CreateCoursesInteractor,
)
from course_management.interactors.dtos import LevelEnum, CourseCategoryEnum
from course_management.tests.factories.interactor_factories import (
    CourseDTOFactory,
    CreateCourseDTOFactory,
)

faker = Faker()
Faker.seed(1)


@pytest.fixture(autouse=True)
def reset_factories():
    CourseDTOFactory.reset_sequence(0)
    CreateCourseDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def storage():
    s = Mock()
    s.get_title_course_ids.return_value = []
    s.get_course_ids_by_title.return_value = []
    yield s
    s.reset_mock()


@pytest.fixture
def interactor(storage):
    return CreateCoursesInteractor(course_storage=storage)


@pytest.mark.django_db
class TestCreateCourses:
    def test_create_courses_successfully(self, interactor, storage, snapshot):
        # ARRANGE
        input_courses = CreateCourseDTOFactory.build_batch(2)
        storage.get_course_ids_by_title.return_value = []

        expected = [
            CourseDTOFactory(
                course_id=f"C000{i + 1}",
                title=course.title,  # FIXED
                description=course.description,
                category=course.category,
                level="BEGINNER",
                average_rating=0,
            )
            for i, course in enumerate(input_courses)
        ]

        storage.create_courses.return_value = expected

        # ACT
        result = interactor.create_courses(input_courses)

        # ASSERT SNAPSHOT
        snapshot.assert_match(
            repr(result),
            "create_courses_success_snapshot.json",
        )

    def test_duplicate_titles_raises(self, interactor, snapshot):
        title = "Python 101"
        courses = [
            CreateCourseDTOFactory.build(title=title),
            CreateCourseDTOFactory.build(title=title),
        ]

        with pytest.raises(DuplicateTitlesFound) as exc:
            interactor.create_courses(courses)

        assert exc.value.titles == [title]

        snapshot.assert_match(
            json.dumps(exc.value.titles, sort_keys=True, indent=2),
            "duplicate_titles_snapshot.json",
        )

    @pytest.mark.parametrize("bad_level", [None])
    def test_invalid_level_raises(self, interactor, bad_level, snapshot):
        course = CreateCourseDTOFactory.create(level=bad_level)

        with pytest.raises(UnexpectedLevelTypeFound) as exc:
            interactor.create_courses([course])

        snapshot.assert_match(
            json.dumps(exc.value.level_types, sort_keys=True, indent=2),
            f"invalid_level_{bad_level or 'none'}_snapshot.json",
        )

    def test_title_already_exists_raises(self, interactor, storage, snapshot):
        existing_course_id = "C9999"
        storage.get_course_ids_by_title.return_value = [existing_course_id]
        course = CreateCourseDTOFactory.build(title="Django Pro")

        with pytest.raises(DuplicateCourseTitleFound) as exc:
            interactor.create_courses([course])

        assert exc.value.course_ids == [existing_course_id]

        snapshot.assert_match(
            json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
            "existing_title_snapshot.json",
        )
