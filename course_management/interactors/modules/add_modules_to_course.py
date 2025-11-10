from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import ModuleDTO, \
    CreateModuleDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface


class AddModulesToCourseInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface,
                 module_storage: ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def add_modules_to_course(self, course_id: str,
                              modules: list[ModuleDTO]) -> list[
        ModuleDTO]:
        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)

        module_ids = [obj.module_id for obj in modules]
        self.check_modules_exist_in_db(module_ids=module_ids,
                                       module_storage=self.module_storage)

        return self.module_storage.add_modules_to_course(course_id=course_id,
                                                         modules=modules)
