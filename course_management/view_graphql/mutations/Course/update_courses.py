import graphene
from course_management.view_graphql.types.input_types import UpdateCoursesParams
from course_management.view_graphql.types.types import CourseType, CoursesType
from course_management.view_graphql.types.error_types import (
    DuplicateTitlesInRequest,
    TitleAlreadyExistsInDB,
    InvalidLevelType,
    DuplicateCourseIdsInRequest,
    CourseIdsNotFound,
)
from course_management.view_graphql.types.response_type import UpdateCoursesResponse
from course_management.interactors.course.update_courses import UpdateCoursesInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.interactors.dtos import UpdateCourseDTO
from course_management.models import Course as DjangoCourse
from course_management.exceptions.custom_exceptions import (
    DuplicateTitlesFound,
    DuplicateCourseTitleFound,
    UnexpectedLevelTypeFound,
    DuplicateCourseIdsFound,
    NotInDBCourseIdsFound,
)
from course_management.storages.feedback_storage import FeedbackStorage


class UpdateCourses(graphene.Mutation):
    class Arguments:
        params = UpdateCoursesParams(required=True)

    Output = UpdateCoursesResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            dtos = []
            for item in params.courses:
                category = DjangoCourse.CourseCategoryEnum(item.category) if item.category else None
                level = DjangoCourse.LevelEnum(item.level) if item.level else None

                dto = UpdateCourseDTO(
                    course_id=item.course_id,
                    title=item.title,
                    description=item.description,
                    category=category,
                    level=level,
                )
                dtos.append(dto)

            updated_dtos = UpdateCoursesInteractor(course_storage=CourseStorage(),feedback_storage=FeedbackStorage()).update_courses(dtos)

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
                for d in updated_dtos
            ]

            return CoursesType(courses=courses)

        except DuplicateTitlesFound as e:
            return DuplicateTitlesInRequest(titles=e.titles)
        except DuplicateCourseTitleFound as e:
            return TitleAlreadyExistsInDB(course_ids=e.course_ids)
        except UnexpectedLevelTypeFound as e:
            level_types = e.level_types or []
            level_types = [str(lt) for lt in level_types if lt is not None]
            return InvalidLevelType(level_types=level_types)
        except DuplicateCourseIdsFound as e:
            return DuplicateCourseIdsInRequest(course_ids=e.course_ids)
        except NotInDBCourseIdsFound as e:
            return CourseIdsNotFound(course_ids=e.course_ids)