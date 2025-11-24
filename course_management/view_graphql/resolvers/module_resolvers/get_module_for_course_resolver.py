from course_management.exceptions import custom_exceptions
from course_management.interactors.modules.get_modules_for_course import \
    GetModulesForCoursesInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.view_graphql.types.error_types import \
    CourseIdsNotInDB
from course_management.view_graphql.types.types import ModuleType, ModuleList


def get_course_modules_resolver(root,info,params):

    course_ids = params.course_ids

    course_storage = CourseStorage()
    module_storage = ModuleStorage()

    interactor = GetModulesForCoursesInteractor(
        course_storage=course_storage,
        module_storage=module_storage
    )

    try:
        modules_dto_list = interactor.get_modules_for_course(
            course_ids=course_ids)

        gql_modules = [
            ModuleType(
                module_id=m.module_id,
                module_title=m.module_title,
                description=m.description,
                course_id=m.course_id,
                order=m.order,
                estimated_duration_in_mins=m.estimated_duration
            )
            for m in modules_dto_list
        ]

        return ModuleList(modules=gql_modules)

    except custom_exceptions.NotInDBCourseIdsFound as e:
        return CourseIdsNotInDB(course_ids=e.course_ids)



