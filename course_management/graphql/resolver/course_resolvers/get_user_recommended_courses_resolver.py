from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.interactors.course.get_recommend_courses import \
    GetRecommendCoursesInteractor

from course_management.storages.course_storage import CourseStorage
from course_management.storages.enrollment_storage import EnrollmentStorage

from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType
from course_management.view_graphql.types.types import CoursesType, CourseType


def get_user_recommended_courses_resolver(root, info, params):
    user_id = params.user_id

    enrollment_storage = EnrollmentStorage()
    user_storage = UserStorage()
    course_storage = CourseStorage()

    interactor = GetRecommendCoursesInteractor(
        user_storage=user_storage, course_storage=course_storage,
        enrollment_storage=enrollment_storage)

    try:
        output_data = interactor.get_recommended_courses(user_id=user_id)

        result = [CourseType(
                    course_id=c.course_id,
                    title=c.title,
                    description=c.description,
                    category=c.category,
                    level=c.level,
                    average_rating=c.average_rating,
                    estimated_duration=c.estimated_duration,
                ) for c in output_data
        ]
        return CoursesType(courses=result)

    except UserNotFound as e:
        return UserNotFoundType(
            user_id=e.user_id
        )
