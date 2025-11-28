import graphene

from course_management.view_graphql.types.input_types import GetCoursesParams
from course_management.view_graphql.types.types import CourseType, CoursesType
from course_management.view_graphql.types.error_types import \
    DuplicateCourseIdsInRequest, CourseIdsNotFound
from course_management.view_graphql.types.response_type import \
    GetCoursesResponse
from course_management.interactors.course.get_courses_interactor import \
    GetCoursesInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.exceptions.custom_exceptions import \
    DuplicateCourseIdsFound, NotInDBCourseIdsFound


def resolve_get_courses(root, info, params):
    try:
        dtos = GetCoursesInteractor(
            course_storage=CourseStorage()).get_courses(params.course_ids)
        courses = [
            CourseType(
                course_id=d.course_id,
                title=d.title,
                description=d.description,
                category=d.category,
                level=d.level,
                average_rating=d.average_rating,
                estimated_duration=d.estimated_duration,
            )
            for d in dtos
        ]
        return CoursesType(courses=courses)

    except DuplicateCourseIdsFound as e:
        return DuplicateCourseIdsInRequest(course_ids=e.course_ids)
    except NotInDBCourseIdsFound as e:
        return CourseIdsNotFound(course_ids=e.course_ids)
