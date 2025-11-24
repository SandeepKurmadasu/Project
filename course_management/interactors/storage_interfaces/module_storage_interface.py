from abc import ABC, abstractmethod

from course_management.interactors.dtos import ModuleDTO, \
    CreateModuleDTO, \
    UpdateModuleDTO


class ModuleStorageInterface(ABC):

    @abstractmethod
    def get_modules_for_courses(self, course_ids: list[str]) -> list[
        ModuleDTO]:
        pass

    @abstractmethod
    def create_modules(self, modules: list[CreateModuleDTO]) -> list[
        ModuleDTO]:
        pass

    @abstractmethod
    def update_modules(self, modules: list[UpdateModuleDTO]) -> list[
        ModuleDTO]:
        pass

    @abstractmethod
    def get_db_existing_module_ids(self, module_ids: list[str]) -> list[str]:
        pass

    @abstractmethod
    def add_modules_to_course(self, course_id: str,
                              module_ids: list[str]) -> list[
        ModuleDTO]:
        pass

    @abstractmethod
    def get_module_ids_for_titles(self, titles: list[str]) -> list[str]:
        pass

    @abstractmethod
    def get_course_modules(self, course_id: str) -> list[ModuleDTO]:
        pass

    @abstractmethod
    def get_modules(self, module_ids: list[str]) -> list[ModuleDTO]:
        pass
