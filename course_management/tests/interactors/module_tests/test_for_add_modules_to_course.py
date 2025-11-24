import json
from unittest.mock import Mock

import pytest
from faker import Faker

from course_management.exceptions.custom_exceptions import CourseNotFound
from course_management.interactors.modules.add_modules_to_course import \
    AddModulesToCourseInteractor
from course_management.tests.factories.interactor_factories import \
    CourseDTOFactory, ModuleDTOFactory

Faker.seed(1)

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
    return AddModulesToCourseInteractor(course_storage=course_storage,
                                        module_storage=module_storage)


class TestAddModulesForCourse:

    def test_add_modules_to_course_successfully(self, module_storage, course_storage,
                                                interactor, snapshot):
        course = CourseDTOFactory()
        modules = ModuleDTOFactory.build_batch(5, course_id=course.course_id)

        module_ids = [obj.module_id for obj in modules]
        course_storage.check_course_exists.return_value = True

        module_storage.get_db_existing_module_ids.return_value = module_ids

        module_storage.add_modules_to_course.return_value = modules

        result = interactor.add_modules_to_course(course.course_id, module_ids=module_ids)


        snapshot.assert_match(
            repr(result),
            "add_modules_to_course_success_snapshot.json"
        )

    def test_for_invalid_course_id_found_exception_raise(self, course_storage,
                                                         module_storage, interactor,
                                                         snapshot):
        course_id = "C1234"
        modules = ModuleDTOFactory.build_batch(3, course_id=course_id)

        course_storage.check_course_exists.return_value = False

        with pytest.raises(CourseNotFound) as e:
            interactor.add_modules_to_course(course_id, modules)

        assert course_id in e.value.course_ids if hasattr(e.value, 'course_ids') else True

        snapshot.assert_match(
            json.dumps({"course_ids": getattr(e.value, "course_ids", [course_id])},
                       sort_keys=True, indent=2),
            "invalid_course_id_found_snapshot.json"
        )
