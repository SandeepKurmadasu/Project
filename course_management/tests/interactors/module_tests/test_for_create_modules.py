import json
import pytest
from unittest.mock import Mock

from faker import Faker

Faker.seed(42)

from course_management.exceptions.custom_exceptions import \
    DuplicateTitlesFound, \
    DuplicateCourseTitleFound, AlreadyExistedTitlesFound
from course_management.interactors.modules.create_modules_interactor import \
    CreateModulesInteractor
from course_management.tests.factories.interactor_factories import \
    ModuleDTOFactory, \
    CreateModuleDTOFactory


@pytest.fixture
def module_storage():
    s = Mock()
    s.get_course_modules.return_value = []
    return s


@pytest.fixture
def interactor(module_storage):
    return CreateModulesInteractor(module_storage=module_storage)


class TestCreateModulesInteractor:

    def test_create_modules_successfully(self, interactor, module_storage, snapshot):
        modules = ModuleDTOFactory.build_batch(2)

        module_storage.get_module_ids_for_titles.return_value = []
        module_storage.create_modules.return_value = modules

        result = interactor.create_modules(modules=modules)

        module_storage.create_modules.assert_called_once_with(modules=modules)
        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2),
            "create_modules_success_snapshot.json"
        )

    def test_duplicate_input_titles_raise(self, interactor, snapshot):
        modules = ModuleDTOFactory.build_batch(2)
        for each_module in modules:
            each_module.module_title = modules[0].module_title

        with pytest.raises(DuplicateTitlesFound) as e:
            interactor.create_modules(modules=modules)

        snapshot.assert_match(
            json.dumps({"titles": e.value.titles}, sort_keys=True, indent=2),
            "duplicate_input_titles_snapshot.json"
        )

    def test_existing_titles_found_exception_raise(self, interactor, module_storage,
                                                   snapshot):
        CreateModuleDTOFactory.reset_sequence(0)

        modules = [
            CreateModuleDTOFactory.build(module_title="Title A"),
            CreateModuleDTOFactory.build(module_title="Title B")
        ]
        existing_module_ids = ["M0001"]

        module_storage.get_module_ids_for_titles.return_value = existing_module_ids

        with pytest.raises(AlreadyExistedTitlesFound) as e:
            interactor.create_modules(modules=modules)



        # Snapshot
        snapshot.assert_match(
            repr(e.value.module_ids),
            "existing_titles_found_snapshot.json"
        )
