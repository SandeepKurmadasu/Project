import json
import pytest
from unittest.mock import Mock

from faker import Faker

from course_management.exceptions.custom_exceptions import \
    NotInDBCourseIdsFound, DBNotFoundedModuleIds

Faker.seed(1)
from course_management.interactors.modules.update_modules_interactor import \
    UpdateModulesInteractor
from course_management.tests.factories.interactor_factories import \
    UpdateModuleDTOFactory, \
    ModuleDTOFactory


@pytest.fixture
def course_storage():
    s = Mock()
    s.check_course_exists.return_value = True
    return s


@pytest.fixture
def module_storage():
    s = Mock()
    s.check_module_exists.return_value = True
    return s


@pytest.fixture
def interactor(course_storage, module_storage):
    return UpdateModulesInteractor(course_storage=course_storage,
                                   module_storage=module_storage)


class TestUpdateModulesInteractor:

    def test_update_modules_successfully(self, interactor, course_storage, module_storage,
                                         snapshot):
        modules = UpdateModuleDTOFactory.build_batch(2)

        course_ids = [m.course_id for m in modules]
        module_ids = [m.module_id for m in modules]

        course_storage.get_valid_course_ids.return_value = course_ids
        module_storage.get_db_existing_module_ids.return_value = module_ids

        module_storage.update_modules.return_value = ModuleDTOFactory.build_batch(2)

        result = interactor.update_modules(modules=modules)

        module_storage.update_modules.assert_called_once_with(modules=modules)

        # Snapshot the result
        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
            "update_modules_success_snapshot.json"
        )

    def test_invalid_course_ids_found_exception_raise(self, interactor, course_storage,
                                                      module_storage, snapshot):
        modules = UpdateModuleDTOFactory.build_batch(2)

        existing_course_ids = [modules[0].course_id]
        course_storage.get_valid_course_ids.return_value = existing_course_ids

        existing_module_ids = [m.module_id for m in modules]
        module_storage.get_valid_module_ids.return_value = existing_module_ids

        with pytest.raises(NotInDBCourseIdsFound) as e:
            interactor.update_modules(modules)

        missing_ids = set([m.course_id for m in modules]) - set(existing_course_ids)
        assert set(e.value.course_ids) == missing_ids

        snapshot.assert_match(
            json.dumps({"course_ids": e.value.course_ids}, sort_keys=True, indent=2),
            "invalid_course_ids_found_snapshot.json"
        )

    def test_invalid_module_ids_found_exception_raise(self, interactor, course_storage,
                                                      module_storage, snapshot):
        modules = UpdateModuleDTOFactory.build_batch(2)

        course_ids = [m.course_id for m in modules]
        course_storage.get_valid_course_ids.return_value = course_ids

        existing_module_ids = [modules[0].module_id]
        module_storage.get_db_existing_module_ids.return_value = existing_module_ids

        module_storage.update_modules.return_value = ModuleDTOFactory.build_batch(
            len(modules))

        with pytest.raises(DBNotFoundedModuleIds) as e:
            interactor.update_modules(modules)

        missing_ids = set([m.module_id for m in modules]) - set(existing_module_ids)
        assert set(e.value.module_ids) == missing_ids

        snapshot.assert_match(
            json.dumps({"module_ids": e.value.module_ids}, sort_keys=True, indent=2),
            "invalid_module_ids_found_snapshot.json"
        )
