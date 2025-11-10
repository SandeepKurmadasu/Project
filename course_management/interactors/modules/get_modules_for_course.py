from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import ModuleDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface


class GetModulesForCoursesInteractor(ValidationMixIn):
    def __init__(self, course_storage: CourseStorageInterface,
                 module_storage: ModuleStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage

    def get_modules_for_course(self, course_ids: list[str]) -> list[ModuleDTO]:
        self.check_course_ids_exist_in_db(course_ids=course_ids,
                                          course_storage=self.course_storage)

        return self.module_storage.get_modules_for_courses(
            course_ids=course_ids)
