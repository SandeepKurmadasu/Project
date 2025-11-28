import graphene

from course_management.exceptions import custom_exceptions
from course_management.interactors.modules.create_modules_interactor import \
    CreateModulesInteractor

from course_management.storages.module_storage import ModuleStorage
from course_management.view_graphql.types.input_types import (
    CreateModulesReqParams
)
from course_management.interactors.dtos import CreateModuleDTO, ModuleDTO
from course_management.view_graphql.types.response_type import (
    ModuleListResponse
)
from course_management.view_graphql.types.types import ModuleType, ModuleList
from course_management.view_graphql.types.error_types import (
    DuplicateTitlesFoundType, AlreadyExistedTitlesFoundType,

)


class CreateModule(graphene.Mutation):
    class Arguments:
        params = CreateModulesReqParams(required=True)

    Output = ModuleListResponse

    @staticmethod
    def mutate(root, info, params):

        dto_list = [
            CreateModuleDTO(
                module_title=each.module_title,
                description=each.description,
                order=each.order
            )
            for each in params.modules
        ]

        module_storage = ModuleStorage()
        interactor = CreateModulesInteractor(module_storage=module_storage)

        try:
            created_modules: list[ModuleDTO] = interactor.create_modules(
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
