from course_management.interactors.dtos import UpdateModuleDTO, ModuleDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.validations import ValidationMixIns


class UpdateModulesInteractor(ValidationMixIns):
    def __init__(self,course_storage : CourseStorageInterface,module_storage : ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage


    def update_modules(self,modules : list[UpdateModuleDTO])->list[ModuleDTO]:
        course_ids = [obj.course_id for obj in modules]
        module_ids = [obj.module_id for obj in modules]

        self.check_if_db_exists_course_ids(course_ids=course_ids, course_storage=self.course_storage)
        self.check_modules_in_db(module_ids=module_ids, module_storage=self.module_storage)

        return self.module_storage.update_modules(modules=modules)



