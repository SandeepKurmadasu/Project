import pytest
from unittest.mock import Mock, patch
import json

from course_management.exceptions.custom_exceptions import (
    DuplicateCourseIdsFound,
    NotInDBCourseIdsFound,
)
from course_management.interactors.course.get_courses_interactor import \
    GetCoursesInteractor
from course_management.interactors.dtos import CourseDTO
from course_management.tests.factories.interactor_factories import \
    CourseDTOFactory
from course_management.interactors.storage_interfaces.course_storage_interface import (
    CourseStorageInterface,
)


@pytest.fixture(autouse=True)
def reset_factory():
    CourseDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def course_storage():
    storage = Mock(spec=CourseStorageInterface)
    storage.get_course_ids_by_title.return_value = []
    storage.get_valid_course_ids.return_value = []
    yield storage
    storage.reset_mock()


@pytest.fixture
def interactor(course_storage):
    return GetCoursesInteractor(course_storage=course_storage)


class TestGetCourses:

    def test_for_get_courses_successfully(self, interactor, course_storage,
                                          snapshot):
        courses = CourseDTOFactory.build_batch(3)
        course_ids = [obj.course_id for obj in courses]

        course_storage.get_valid_course_ids.return_value = course_ids
        course_storage.get_courses.return_value = [
            CourseDTO(
                course_id=each_course.course_id,
                title=each_course.title,
                description=each_course.description,
                category=each_course.category,
                level=each_course.level,
                average_rating=each_course.average_rating,
                estimated_duration=each_course.estimate_duration_in_mins
            )
            for each_course in courses
        ]

        # Act
        result = interactor.get_courses(course_ids)

        # Assert
        course_storage.get_courses.assert_called_once_with(
            course_ids=course_ids)  # ✅ Fixed
        assert isinstance(result, list)
        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
            "get_courses_success_snapshot.json"
        )

    def test_duplicate_course_ids_found_raise_exception(self, interactor,
                                                        course_storage,
                                                        snapshot):
        courses = CourseDTOFactory.create_batch(3)
        create_courses = []
        course_ids = []
        for each_course in courses:
            each_course.course_id = courses[0].course_id
            course_ids.append(each_course.course_id)
            create_courses.append(each_course)

        course_storage.get_valid_course_ids.return_value = course_ids
        course_storage.get_courses.return_value = [
            CourseDTO(
                course_id=each_course.course_id,
                title=each_course.title,
                description=each_course.description,
                category=each_course.category,
                level=each_course.level,
                average_rating=each_course.average_rating,
                estimated_duration=each_course.estimate_duration_in_mins
            )
            for each_course in courses
        ]

        # Act & Patch - mock the validation mixin to raise exception
        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_duplicate_course_ids"
        ) as mock_method:
            mock_method.side_effect = DuplicateCourseIdsFound(
                course_ids=course_ids)
            with pytest.raises(DuplicateCourseIdsFound) as exc:
                interactor.get_courses(course_ids)

        # Assert
        assert exc.value.course_ids == course_ids
        snapshot.assert_match(
            json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
            "duplicate_course_ids_snapshot.json"
        )

    def test_course_ids_not_found_raise_exception(self, interactor,
                                                  course_storage,
                                                  snapshot):
        courses = CourseDTOFactory.create_batch(3)
        course_ids = [obj.course_id for obj in courses]

        course_storage.get_courses.return_value = [
            CourseDTO(
                course_id=each_course.course_id,
                title=each_course.title,
                description=each_course.description,
                category=each_course.category,
                level=each_course.level,
                average_rating=each_course.average_rating,
                estimated_duration=each_course.estimate_duration_in_mins
            )
            for each_course in courses
        ]

        with patch(
                "course_management.interactors.common_validation_mixin.ValidationMixIn.check_course_ids_exist_in_db"
        ) as mock_method:
            mock_method.side_effect = NotInDBCourseIdsFound(
                course_ids=course_ids)
            with pytest.raises(NotInDBCourseIdsFound) as exc:
                interactor.get_courses(course_ids)

        # Assert
        assert exc.value.course_ids == course_ids
        snapshot.assert_match(
            json.dumps(exc.value.course_ids, sort_keys=True, indent=2),
            "not_in_db_course_ids_snapshot.json"
        )
