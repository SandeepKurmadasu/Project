import graphene

from course_management.exceptions import custom_exceptions

from course_management.interactors.modules.update_modules_interactor import \
    UpdateModulesInteractor
from course_management.storages.course_storage import CourseStorage

from course_management.storages.module_storage import ModuleStorage
from course_management.view_graphql.types.input_types import (
    UpdateModulesListReqParams
)
from course_management.interactors.dtos import ModuleDTO, UpdateModuleDTO
from course_management.view_graphql.types.response_type import (
    ModuleListResponse
)
from course_management.view_graphql.types.types import ModuleType, ModuleList
from course_management.view_graphql.types.error_types import (
    DuplicateTitlesFoundType, AlreadyExistedTitlesFoundType, CourseIdsNotInDB,
    ModuleIdsNotFoundInDBType,

)


class UpdateModule(graphene.Mutation):
    class Arguments:
        params = UpdateModulesListReqParams(required=True)

    Output = ModuleListResponse

    @staticmethod
    def mutate(root, info, params):

        dto_list = [
            UpdateModuleDTO(
                module_title=each.module_title,
                description=each.description,
                course_id=each.course_id,
                module_id=each.module_id,
                order=each.order
            )
            for each in params.update_modules
        ]

        module_storage = ModuleStorage()
        course_storage = CourseStorage()
        interactor = UpdateModulesInteractor(module_storage=module_storage,
                                             course_storage=course_storage)

        try:
            created_modules: list[ModuleDTO] = interactor.update_modules(
                dto_list)

            gql_modules = [
                ModuleType(
                    module_id=m.module_id,
                    module_title=m.module_title,
                    description=m.description,
                    course_id=m.course_id,
                    order=m.order,
                    estimated_duration_in_mins=m.estimated_duration
                )
                for m in created_modules
            ]

            return ModuleList(modules=gql_modules)

        except custom_exceptions.DuplicateTitlesFound as e:
            return DuplicateTitlesFoundType(
                titles=e.titles
            )

        except custom_exceptions.AlreadyExistedTitlesFound as e:
            return AlreadyExistedTitlesFoundType(
                module_ids=e.module_ids
            )

        except custom_exceptions.NotInDBCourseIdsFound as e:
            return CourseIdsNotInDB(
                course_ids=e.course_ids
            )

        except custom_exceptions.DBNotFoundedModuleIds as e:
            return ModuleIdsNotFoundInDBType(
                module_ids=e.module_ids
            )
