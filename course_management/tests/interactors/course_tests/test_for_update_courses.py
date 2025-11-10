import pytest
from unittest.mock import patch, create_autospec, MagicMock
import json
from faker import Faker

from course_management.exceptions import custom_exceptions
from course_management.interactors.course.update_courses import \
    UpdateCoursesInteractor
from course_management.interactors.dtos import CourseDTO
from course_management.interactors.storage_interfaces.course_storage_interface import (
    CourseStorageInterface,
)
from course_management.tests.factories.interactor_factories import \
    CourseDTOFactory


@pytest.fixture(autouse=True)
def set_faker_seed():
    Faker.seed(0)


class TestUpdateCourses:

    def setup_method(self):
        self.course_storage = create_autospec(CourseStorageInterface)
        self.feedback_storage = MagicMock()
        self.interactor = UpdateCoursesInteractor(
            course_storage=self.course_storage,
            feedback_storage=self.feedback_storage
        )

    def test_update_courses_successfully(self, snapshot):
        courses = CourseDTOFactory.build_batch(3)

        self.course_storage.get_course_ids_by_title.return_value = []
        self.course_storage.get_valid_course_ids.return_value = [obj.course_id
                                                                 for obj in
                                                                 courses]
        self.course_storage.update_courses.return_value = [
            CourseDTO(**each_course.__dict__) for each_course in courses
        ]

        result = self.interactor.update_courses(courses=courses)

        self.course_storage.update_courses.assert_called_once_with(courses)

        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
            "update_courses_success_snapshot.json"
        )

    def test_duplicate_titles_found_raise_exception(self, snapshot):
        courses = CourseDTOFactory.build_batch(3)
        titles = []
        for each_course in courses:
            each_course.title = courses[0].title
            titles.append(each_course.title)

        self.course_storage.get_course_ids_by_title.return_value = []

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_duplicate_course_titles"
        ) as mock_method:
            mock_method.side_effect = custom_exceptions.DuplicateTitlesFound(
                titles=list(set(titles)))
            with pytest.raises(custom_exceptions.DuplicateTitlesFound) as e:
                self.interactor.update_courses(courses=courses)

        assert e.value.titles == list(set(titles))
        snapshot.assert_match(
            json.dumps(e.value.titles, sort_keys=True, indent=2),
            "duplicate_update_titles_snapshot.json"
        )

    def test_existing_titles_found_raise_exception(self, snapshot):
        CourseDTOFactory.reset_sequence(0)
        courses = CourseDTOFactory.build_batch(3)

        self.course_storage.get_course_ids_by_title.return_value = [
            courses[0].title]

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_existing_titles"
        ) as mock_method:
            mock_method.side_effect = custom_exceptions.DuplicateCourseTitleFound(
                course_ids=courses[0].course_id)
            with pytest.raises(
                    custom_exceptions.DuplicateCourseTitleFound) as e:
                self.interactor.update_courses(courses=courses)

        assert e.value.course_ids == courses[0].course_id
        snapshot.assert_match(
            json.dumps(e.value.course_ids, sort_keys=True, indent=2),
            "duplicate_update_titles_snapshot.json"
        )

    def test_invalid_level_found_raise_exception(self, snapshot):
        CourseDTOFactory.reset_sequence(0)
        courses = CourseDTOFactory.build_batch(3)

        self.course_storage.get_course_ids_by_title.return_value = []

        level_types = []
        for each_course in courses:
            each_course.level = "baba"
            level_types.append(each_course.level)

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_invalid_level_type"
        ) as mock_method:
            mock_method.side_effect = custom_exceptions.UnexpectedLevelTypeFound(
                level_types=level_types)
            with pytest.raises(
                    custom_exceptions.UnexpectedLevelTypeFound) as e:
                self.interactor.update_courses(courses=courses)

        assert e.value.level_types == level_types
        snapshot.assert_match(
            json.dumps(e.value.level_types, sort_keys=True, indent=2),
            "invalid_level_snapshot.json"
        )

    def test_not_existed_course_ids_found_raise_exception(self, snapshot):
        CourseDTOFactory.reset_sequence(0)
        courses = CourseDTOFactory.build_batch(3)
        course_ids = [each_course.course_id for each_course in courses]

        self.course_storage.get_course_ids_by_title.return_value = []
        self.course_storage.get_valid_course_ids.return_value = []

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_course_ids_exist_in_db"
        ) as mock_method:
            mock_method.side_effect = custom_exceptions.NotInDBCourseIdsFound(
                course_ids=course_ids)
            with pytest.raises(custom_exceptions.NotInDBCourseIdsFound) as e:
                self.interactor.update_courses(courses=courses)

        assert e.value.course_ids == course_ids
        snapshot.assert_match(
            json.dumps(e.value.course_ids, sort_keys=True, indent=2),
            "not_existed_course_ids_snapshot.json"
        )
