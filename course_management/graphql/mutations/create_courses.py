import graphene
from ..types.input_types import CreateCoursesInput
from ..types.types import CoursesType

from course_management.interactors.course.create_course_interactor import CreateCoursesInteractor, CreateCourseDTO
from course_management.storages.course_storage import CourseStorage
from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    DuplicateCourseTitleFound,
    UnexpectedLevelTypeFound,
)
from ..types.error_types import DuplicateTitlesInRequest, TitleAlreadyExistsInDB, InvalidLevelType
from ..types.response_types import CreateCoursesResponse


class CreateCourses(graphene.Mutation):
    class Arguments:
        courses = graphene.List(CreateCoursesInput, required=True)

    Output = CreateCoursesResponse

    @staticmethod
    def mutate(root, info, courses):
        from course_management.models import Course as DjangoCourse

        try:
            dtos = [
                CreateCourseDTO(
                    title=c.title,
                    description=c.description,
                    category=getattr(DjangoCourse.CourseCategoryEnum, c.category.name),
                    level=getattr(DjangoCourse.LevelEnum, c.level.name),
                )
                for c in courses
            ]

            created_dtos = CreateCoursesInteractor(course_storage=CourseStorage()).create_courses(dtos)

            course_objs = [
                CoursesType(
                    course_id=d.course_id,
                    title=d.title,
                    description=d.description,
                    category=d.category.value,
                    level=d.level.value,
                    average_rating=d.average_rating,
                    estimated_duration=d.estimated_duration,
                )
                for d in created_dtos
            ]

            return CreateCoursesResponse(courses=course_objs)

        except DuplicateTitlesFound as e:
            return DuplicateTitlesInRequest(titles=e.titles)
        except DuplicateCourseTitleFound as e:
            return TitleAlreadyExistsInDB(course_ids=e.course_ids)
        except UnexpectedLevelTypeFound as e:
            return InvalidLevelType(level_types=e.level_types)