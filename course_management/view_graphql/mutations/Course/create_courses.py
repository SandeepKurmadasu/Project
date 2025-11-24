import graphene

from course_management.interactors.dtos import CourseCategoryEnum, LevelEnum
from course_management.view_graphql.types.input_types import CreateCourseInput
from course_management.view_graphql.types.types import CourseType, CoursesType

from course_management.interactors.course.create_course_interactor import CreateCoursesInteractor, CreateCourseDTO
from course_management.storages.course_storage import CourseStorage
from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    DuplicateCourseTitleFound,
    UnexpectedLevelTypeFound,
)
from course_management.view_graphql.types.error_types import DuplicateTitlesInRequest, TitleAlreadyExistsInDB, InvalidLevelType
from course_management.view_graphql.types.response_type import CreateCoursesResponse


class CreateCourses(graphene.Mutation):
    class Arguments:
        courses = graphene.List(CreateCourseInput, required=True)

    Output = CreateCoursesResponse

    @staticmethod
    def mutate(root, info, courses):

        try:
            dtos = [
                CreateCourseDTO(
                    title=c.title,
                    description=c.description,
                    category=CourseCategoryEnum[c.category],
                    level=LevelEnum[c.level],
                )
                for c in courses
            ]

            created_dtos = CreateCoursesInteractor(course_storage=CourseStorage()).create_courses(dtos)

            course_objs = [
                CourseType(
                    course_id=d.course_id,
                    title=d.title,
                    description=d.description,
                    category=d.category,
                    level=d.level,
                    average_rating=d.average_rating,
                    estimated_duration=d.estimated_duration,
                )
                for d in created_dtos
            ]

            return CoursesType(courses=course_objs)

        except DuplicateTitlesFound as e:
            return DuplicateTitlesInRequest(titles=e.titles)
        except DuplicateCourseTitleFound as e:
            return TitleAlreadyExistsInDB(course_ids=e.course_ids)
        except UnexpectedLevelTypeFound as e:
            return InvalidLevelType(level_types=e.level_types)