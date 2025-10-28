from course_management.interactors.dtos import ModuleDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.validations import ValidationMixIns

class AddModulesToCourseInteractor(ValidationMixIns):

    def __init__(self,course_storage : CourseStorageInterface,module_storage : ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def add_modules_to_course(self,course_id : str,modules : list[ModuleDTO])->list[ModuleDTO]:
        self.check_if_course_exists(course_id=course_id,course_storage=self.course_storage)

        module_ids = [obj.module_id for obj in modules]
        self.check_modules_in_db(module_ids=module_ids, module_storage=self.module_storage)

        return self.module_storage.add_modules_to_course(course_id=course_id,modules=modules)



