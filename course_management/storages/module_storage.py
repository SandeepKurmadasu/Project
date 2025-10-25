from course_management.models import Module
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface

class ModuleStorage(ModuleStorageInterface):

    def get_course_modules(self,course_id : str) ->list:
        return list(Module.objects.filter(course_id=course_id))
