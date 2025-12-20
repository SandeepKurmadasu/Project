from course_management.interactors.dtos import CourseDTO
from course_management.interactors.presenter_interfaces.create_courses_presenter_interface import \
    CreateCoursesPresenterInterface
from course_management.view_graphql.types.types import CoursesType, CourseType


class CreateCoursesPresenter(CreateCoursesPresenterInterface):

    def present_courses(self, courses: list[CourseDTO]) -> CoursesType:
        course_objs = [
            CourseType(
                course_id=d.course_id,
                title=d.title,
                description=d.description,
                category=d.category.value,
                level=d.level.value,
                average_rating=d.average_rating,
                estimated_duration=d.estimated_duration,
            )
            for d in courses
        ]

        return CoursesType(courses=course_objs)
