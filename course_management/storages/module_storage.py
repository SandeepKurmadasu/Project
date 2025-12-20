import uuid

from course_management.interactors.common_validation_mixin import storage_cache
from course_management.interactors.dtos import CreateModuleDTO, \
    ModuleDTO, \
    UpdateModuleDTO
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface
from course_management.models import Module, Course


class ModuleStorage(ModuleStorageInterface):

    @storage_cache(timeout=5*60)
    def get_modules_for_courses(self, course_ids: list[str]) -> list[
        ModuleDTO]:
        modules = Module.objects.filter(course_id__in=course_ids)

        return [ModuleDTO(
            module_id=each_module.module_id,
            course_id=each_module.course.course_id,
            module_title=each_module.module_title,
            description=each_module.description,
            order=each_module.order,
            estimated_duration=each_module.estimated_duration_in_min
        ) for each_module in modules]

    def create_modules(self, modules: list[CreateModuleDTO]) -> list[
        ModuleDTO]:
        module_objs = [
            Module(
                module_title=each.module_title,
                description=each.description,
                order=each.order
            )
            for each in modules
        ]
        created_modules = Module.objects.bulk_create(module_objs)

        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=str(obj.course.pk) if obj.course else None,
            module_title=obj.module_title,
            description=obj.description,
            order=obj.order,
            estimated_duration=obj.estimated_duration_in_min
        ) for obj in created_modules]

    def update_modules(self, modules: list[UpdateModuleDTO]) -> list[
        ModuleDTO]:
        module_ids = [each_module.module_id for each_module in modules]
        updated_modules = [
            Module(
                module_id=each_module.module_id,
                module_title=each_module.module_title,
                description=each_module.description,
                order=each_module.order
            ) for each_module in modules
        ]
        Module.objects.bulk_update(updated_modules,
                                   fields=['module_title', 'description',
                                           'order'])
        get_modules = Module.objects.filter(module_id__in=module_ids)

        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            order=obj.order,
            estimated_duration=obj.estimated_duration_in_min
        ) for obj in get_modules]

    def get_db_existing_module_ids(self, module_ids: list[str]) -> list[str]:
        return list(
            Module.objects.filter(module_id__in=module_ids).values_list(
                'module_id',
                flat=True))

    def add_modules_to_course(self, course_id: str,
                              module_ids: list[str]) -> list[ModuleDTO]:
        course = Course.objects.get(course_id=course_id)
        modules_data = []
        for each_module in module_ids:
            modules_data.append(Module(
                module_id=each_module,
                course=course
            ))

        Module.objects.bulk_update(modules_data, fields=['course'])

        modules = self.get_modules(module_ids=module_ids)

        return modules

    def get_module_ids_for_titles(self, titles: list[str]) -> list[str]:
        return list(Module.objects.filter(module_title__in=titles).values_list(
            'module_id',
            flat=True))

    def get_course_modules(self, course_id: str) -> list[ModuleDTO]:
        modules = Module.objects.filter(course_id=course_id)

        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            order=obj.order,
            estimated_duration=obj.estimated_duration_in_min
        ) for obj in modules]

    def get_modules(self, module_ids: list[str]) -> list[ModuleDTO]:
        modules = Module.objects.filter(module_id__in=module_ids)

        return [ModuleDTO(
            module_id=obj.module_id,
            course_id=obj.course.course_id,
            module_title=obj.module_title,
            description=obj.description,
            order=obj.order,
            estimated_duration=obj.estimated_duration_in_min
        ) for obj in modules]
