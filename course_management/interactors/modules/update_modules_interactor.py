from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import ModuleDTO, \
    UpdateModuleDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface


class UpdateModulesInteractor(ValidationMixIn):
    def __init__(self, course_storage: CourseStorageInterface,
                 module_storage: ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def update_modules(self, modules: list[UpdateModuleDTO]) -> list[
        ModuleDTO]:
        course_ids = [obj.course_id for obj in modules]
        module_ids = [obj.module_id for obj in modules]

        self.check_course_ids_exist_in_db(course_ids=course_ids,
                                          course_storage=self.course_storage)
        self.check_modules_exist_in_db(module_ids=module_ids,
                                       module_storage=self.module_storage)

        return self.module_storage.update_modules(modules=modules)
