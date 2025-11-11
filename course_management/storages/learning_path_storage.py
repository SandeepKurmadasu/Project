from course_management.interactors.dtos import (
    CreateCourseLearningPathDTO,
    LearningPathForCourseDTO,
)
from course_management.interactors.storage_interfaces.learning_path_storage_interface import (
    LearningPathStorageInterface,
)
from course_management.models import CourseLearningPath, Course


class LearningPathStorage(LearningPathStorageInterface):
    def create_course_learning_path(self,
                                    course_id: str) -> LearningPathForCourseDTO:

        course = Course.objects.get(course_id=course_id)

        learning_path = CourseLearningPath.objects.create(course=course)

        return LearningPathForCourseDTO(
            learning_path_id=learning_path.learning_path_id,
            course_id=course.course_id,
            course_title=course.title,
            total_units=0,
            estimated_total_duration_in_minutes=course.estimated_duration_in_min,
            learning_units=[],
        )

    def get_course_learning_path(self,
                                 learning_path_id: str) -> LearningPathForCourseDTO:
        lp = CourseLearningPath.objects.select_related("course").get(
            learning_path_id=learning_path_id
        )

        return LearningPathForCourseDTO(
            learning_path_id=lp.learning_path_id,
            course_id=lp.course.course_id,
            course_title=lp.course.module_title
            if hasattr(lp.course, "module_title")
            else lp.course.title,
            total_units=lp.course.modules.count(),
            estimated_total_duration_in_minutes=lp.course.estimated_duration_in_mins,
            learning_units=[],
        )

    def learning_path_exist(self, learning_path_id: str) -> bool:

        return CourseLearningPath.objects.filter(
            learning_path_id=learning_path_id
        ).exists()

    def get_latest_learning_path_by_course_id(
            self, course_id: str) -> LearningPathForCourseDTO | None:

        latest_path = (
            CourseLearningPath.objects.filter(course_id=course_id)
            .order_by("-created_at").first()
        )
        if not latest_path:
            return None

        return LearningPathForCourseDTO(
            learning_path_id=str(latest_path.learning_path_id),
            course_id=str(latest_path.course.course_id),
            course_title=latest_path.course.title,
            total_units=0,  # You can fill from unit storage if needed
            estimated_total_duration_in_minutes=latest_path.course.estimated_duration_in_mins,
            learning_units=[],
        )

    def get_learning_path_by_course_id(
            self, course_id: str) -> LearningPathForCourseDTO | None:

        path = (
            CourseLearningPath.objects.filter(course_id=course_id)
            .order_by("-created_at").first()
        )

        if not path:
            return None

        return LearningPathForCourseDTO(
            learning_path_id=str(path.learning_path_id),
            course_id=str(path.course.course_id),
            course_title=path.course.title,
            total_units=0,
            estimated_total_duration_in_minutes=path.course.estimated_duration_in_mins,
            learning_units=[],
        )
