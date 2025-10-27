from course_management.interactors.dtos import ModuleDTO, CreateModuleDTO, UpdateModuleDTO
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.models import Module, Course


class ModuleStorage(ModuleStorageInterface):

    def get_modules_for_courses(self,course_ids : list[str])->list[ModuleDTO]:
        modules = Module.objects.filter(course_id__in=course_ids)
        return [ModuleDTO(
            module_id=each_module.module_id,
            course_id=each_module.course.course_id,
            module_title=each_module.module_title,
            description=each_module.description,
            estimated_duration=each_module.estimated_duration
        ) for each_module in modules]

    def create_modules(self,modules : list[CreateModuleDTO])->list[ModuleDTO]:
        module_objs = [
            Module(
                module_title=each.module_title,
                description=each.description
            )
            for each in modules
        ]
        created_modules = Module.objects.bulk_create(module_objs)
        return [ ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            estimated_duration=obj.estimated_duration
        ) for obj in created_modules]

    def update_modules(self, modules: list[UpdateModuleDTO]) -> list[ModuleDTO]:
        module_ids = [each_module.module_id for each_module in modules]
        updated_modules=[
            Module(
                module_id=each_module.module_id,
                module_title=each_module.module_title,
                description=each_module.description
            ) for each_module in modules
        ]
        Module.objects.bulk_update(updated_modules,fields=['module_title','description'])
        get_modules = Module.objects.filter(module_id__in=module_ids)
        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            estimated_duration=obj.estimated_duration
        ) for obj in get_modules]

    def get_db_existing_module_ids(self,module_ids : list[str])->list[str]:
        return list(Module.objects.filter(module_id__in=module_ids).values_list('module_id',flat=True))

    def add_modules_to_course(self,course_id : str,modules : list[ModuleDTO])->list[ModuleDTO]:
        course = Course.objects.get(course_id=course_id)
        for each_module in modules:
            each_module.course = course

        Module.objects.bulk_update(modules,fields=['course'])

        return modules

    def get_module_ids_for_titles(self, titles: list[str]) -> list[str]:
        return  list(Module.objects.filter(module_title__in=titles).values_list('module_id',flat=True))

    def get_course_modules(self,course_id : str)->list[ModuleDTO]:
        modules = Module.objects.filter(course_id=course_id)

        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            estimated_duration=obj.estimated_duration
        ) for obj in modules]