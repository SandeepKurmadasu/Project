import json
from unittest.mock import Mock

import pytest

from course_management.exceptions.custom_exceptions import \
    NotInDBCourseIdsFound
from course_management.interactors.modules.get_modules_for_course import \
    GetModulesForCoursesInteractor
from course_management.tests.factories.interactor_factories import \
    CourseDTOFactory, ModuleDTOFactory


@pytest.fixture
def course_storage():
    s = Mock()
    s.get_valid_course_ids.return_value = []
    return s


@pytest.fixture
def module_storage():
    s = Mock()
    s.check_module_exists.return_value = True
    return s


@pytest.fixture
def interactor(course_storage, module_storage):
    return GetModulesForCoursesInteractor(course_storage=course_storage,
                                          module_storage=module_storage)


class TestGetModulesForCourses:

    def test_for_get_modules_for_courses_successfully(self, course_storage, module_storage,
                                                      interactor, snapshot):
        courses = CourseDTOFactory.build_batch(2)
        course_ids = [course.course_id for course in courses]

        course_storage.get_valid_course_ids.return_value = course_ids

        expected_modules = [
            ModuleDTOFactory(course_id=courses[0].course_id),
            ModuleDTOFactory(course_id=courses[1].course_id),

        ]
        module_storage.get_modules_for_courses.return_value = expected_modules

        result = interactor.get_modules_for_course(course_ids)

        module_storage.get_modules_for_courses.assert_called_once_with(
            course_ids=course_ids)

        snapshot.assert_match(
            json.dumps([r.__dict__ if hasattr(r, '__dict__') else r for r in result],
                       sort_keys=True, indent=2),
            "get_modules_for_courses_success_snapshot.json"
        )

    def test_for_invalid_course_ids_found_exception_raise(self, course_storage,
                                                          module_storage, interactor,
                                                          snapshot):
        course_ids = ["C0001", "C0002"]

        existing_course_ids = [course_ids[0]]
        course_storage.get_valid_course_ids.return_value = existing_course_ids

        with pytest.raises(NotInDBCourseIdsFound) as e:
            interactor.get_modules_for_course(course_ids)

        missing_ids = set(course_ids) - set(existing_course_ids)
        assert set(e.value.course_ids) == missing_ids

        snapshot.assert_match(
            json.dumps({"course_ids": list(e.value.course_ids)}, sort_keys=True, indent=2),
            "invalid_course_ids_found_snapshot.json"
        )
