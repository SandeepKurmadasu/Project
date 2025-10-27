from course_management.interactors.dtos import ModuleDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.validations import ValidationMixIns


class GetModulesForCoursesInteractor(ValidationMixIns):
    def __init__(self,course_storage : CourseStorageInterface,module_storage : ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def get_modules_for_course(self,course_ids :list[str])->list[ModuleDTO]:
        self.check_if_db_exists_course_ids(course_ids=course_ids, course_storage=self.course_storage)

        return self.module_storage.get_modules_for_courses(course_ids=course_ids)