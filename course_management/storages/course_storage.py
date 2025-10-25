from course_management.interactors.dtos import CourseDTO, CreateCourseDTO, UpdateCourseDTO, ModuleDTO, TopicDTO, \
    UserTopicCompletionPercentageDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.models import Course


class CourseStorage(CourseStorageInterface):

    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        if not course_ids:
            return []

        course_objects = Course.objects.filter(course_id__in=course_ids)

        course_dtos = []
        for course in course_objects:
            course_dtos.append(
                CourseDTO(
                    course_id=str(course.course_id),  # Convert UUID to string
                    title=course.title,
                    description=course.description,
                    category=course.category,
                    level=course.level,
                    average_rating=course.average_rating,
                    estimated_duration=course.estimated_duration
                )
            )

        return course_dtos

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[CourseDTO]:
        if not courses:
            return []

        course_objects = []
        for c in courses:
            course = Course(
                title=c.title,
                description=c.description,
                category=c.category,
                level=c.level
            )
            course_objects.append(course)

        Course.objects.bulk_create(course_objects)

        course_dtos = []
        for course in course_objects:
            course_dto = CourseDTO(
                course_id=str(course.course_id),  # Convert UUID to string
                title=course.title,
                description=course.description,
                category=course.category,
                level=course.level,
                average_rating=course.average_rating,
                estimated_duration=course.estimated_duration
            )
            course_dtos.append(course_dto)

        return course_dtos

    def get_title_course_ids(self, titles: list[str]) -> list[str]:
        if not titles:
            return []

        course_ids = Course.objects.filter(title__in=titles).values_list('course_id', flat=True)
        return [str(cid) for cid in course_ids]  # Convert UUIDs to strings

    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[CourseDTO]:
        updated_course_dtos = []

        for course_dto in courses:
            course = Course.objects.get(course_id=course_dto.course_id)
            course.title = course_dto.title
            course.description = course_dto.description
            course.category = course_dto.category
            course.level = course_dto.level
            course.save()

            updated_course_dtos.append(
                CourseDTO(
                    course_id=str(course.course_id),  # Convert UUID to string
                    title=course.title,
                    description=course.description,
                    category=course.category,
                    level=course.level,
                    average_rating=course.average_rating,
                    estimated_duration=course.estimated_duration
                )
            )

        return updated_course_dtos

    def get_valid_course_ids(self, course_ids: list[str]) -> list[str]:
        if not course_ids:
            return []
        existing_ids = Course.objects.filter(course_id__in=course_ids).values_list('course_id', flat=True)
        return [str(eid) for eid in existing_ids]  # Convert UUIDs to strings

    def check_course_exists(self, course_id: str) -> bool:
        return Course.objects.filter(course_id=course_id).exists()

    def get_all_course_ids(self) -> list[str]:
        course_ids = Course.objects.values_list('course_id', flat=True)
        return [str(cid) for cid in course_ids]  # Convert UUIDs to strings

    def get_recommend_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        if not course_ids:
            return []

        course_objects = Course.objects.filter(course_id__in=course_ids)
        course_dtos = []

        for c in course_objects:
            course_dtos.append(
                CourseDTO(
                    course_id=str(c.course_id),  # Convert UUID to string
                    title=c.title,
                    description=c.description,
                    category=c.category,
                    level=c.level,
                    average_rating=c.average_rating,
                    estimated_duration=c.estimated_duration
                )
            )
        return course_dtos


    def get_excluded_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        pass

    def get_topics_in_course(self, course_id: str):
        pass

    def get_enum_types(self) -> list[str]:
        pass

    def get_modules_in_course(self, course_id: str) -> list[ModuleDTO]:
        pass

    def get_topics_in_module(self, module_id: str) -> list[TopicDTO]:
        pass

    def get_user_topic_completion_percentages(self, user_id: str, topic_ids: list[str]) -> list[UserTopicCompletionPercentageDTO]:
        pass

    def get_topics_for_modules(self, module_ids: list[str]) -> list[TopicDTO]:
        pass

    def get_topics_in_modules(self, module_ids: list[str]) -> list[TopicDTO]:
        pass



