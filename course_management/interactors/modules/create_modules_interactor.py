from course_management.exceptions.custom_exceptions import DuplicateTitlesFound, DuplicateCourseTitleFound
from course_management.interactors.dtos import CreateModuleDTO, ModuleDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.validations import ValidationMixIns


class CreateModulesInteractor(ValidationMixIns):
    def __init__(self,course_storage : CourseStorageInterface,module_storage : ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def create_modules(self,modules : list[CreateModuleDTO])->list[ModuleDTO]:
        self._check_duplicate_module_titles(modules=modules,module_storage=self.module_storage)
        self._check_existing_module_titles(modules=modules)

        return self.module_storage.create_modules(modules=modules)


    @staticmethod
    def _check_duplicate_module_titles(modules: list[CreateModuleDTO], module_storage: ModuleStorageInterface):
        titles = [obj.module_title for obj in modules]

        duplicate_titles = [
            title for title in titles if titles.count(title) > 1
        ]

        if duplicate_titles:
            raise DuplicateTitlesFound(titles=list(set(duplicate_titles)))


    def _check_existing_module_titles(self,modules: list[CreateModuleDTO]):
        titles = [obj.module_title for obj in modules]

        existing_module_ids = self.module_storage.get_module_ids_for_titles(titles=titles)

        if existing_module_ids:
            raise DuplicateCourseTitleFound(course_ids=existing_module_ids)