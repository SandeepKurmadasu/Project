import graphene

from course_management.exceptions import custom_exceptions
from course_management.interactors.dtos import ModuleDTO
from course_management.interactors.modules.add_modules_to_course import \
    AddModulesToCourseInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.view_graphql.types.input_types import AddModulesToCourseReqParams
from course_management.view_graphql.types.response_type import ModuleListResponse
from course_management.view_graphql.types.types import ModuleType, ModuleList
from course_management.view_graphql.types.error_types import (
    ModuleIdsNotFoundInDBType,
    CourseIdsNotInDB,
)


class AddModulesToCourse(graphene.Mutation):
    class Arguments:
        params = AddModulesToCourseReqParams(required=True)

    Output = ModuleListResponse

    @staticmethod
    def mutate(root, info, params):
        course_storage = CourseStorage()
        module_storage = ModuleStorage()

        interactor = AddModulesToCourseInteractor(
            course_storage=course_storage,
            module_storage=module_storage
        )

        try:
            added_modules: list[ModuleDTO] = interactor.add_modules_to_course(
                course_id=params.course_id,
                module_ids=params.module_ids
            )

            gql_modules = [
                ModuleType(
                    module_id=m.module_id,
                    module_title=m.module_title,
                    description=m.description,
                    course_id=m.course_id,
                    order=m.order,
                    estimated_duration_in_mins=m.estimated_duration
                )
                for m in added_modules
            ]

            return ModuleList(modules=gql_modules)

        except custom_exceptions.DBNotFoundedModuleIds as e:
            return ModuleIdsNotFoundInDBType(module_ids=e.module_ids)

        except custom_exceptions.NotInDBCourseIdsFound as e:
            return CourseIdsNotInDB(course_ids=e.course_ids)
