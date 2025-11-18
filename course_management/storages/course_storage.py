from course_management.interactors.dtos import CourseDTO, \
    CreateCourseDTO, UpdateCourseDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.models import Course


class CourseStorage(CourseStorageInterface):

    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        courses = Course.objects.filter(course_id__in=course_ids)

        return [CourseDTO(
            course_id=course.course_id,
            title=course.title,
            description=course.description,
            category=course.category,
            level=course.level,
            average_rating=course.average_rating,
            estimated_duration=course.estimated_duration_in_min
        ) for course in courses]

    def get_valid_course_ids(self, course_ids: list[str]) -> list[str]:
        # Get all given course ids if exists
        return list(
            Course.objects.filter(course_id__in=course_ids).values_list(
                'course_id', flat=True))

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[
        CourseDTO]:
        course_data = [
            Course(
                title=obj.title,
                description=obj.description,
                category=obj.category,
                level=obj.level
            ) for obj in courses
        ]
        courses = Course.objects.bulk_create(course_data)
        created_courses = [CourseDTO(
            course_id=course.course_id,
            title=course.title,
            description=course.description,
            category=course.category,
            level=course.level,
            average_rating=0,
            estimated_duration=0
        ) for course in courses]
        return created_courses

    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[
        CourseDTO]:
        course_ids = [each_course.course_id for each_course in courses]

        course_objects = list(Course.objects.filter(course_id__in=course_ids))

        dto_map = {dto.course_id: dto for dto in courses}

        for course_obj in course_objects:
            dto = dto_map[course_obj.course_id]
            course_obj.title = dto.title
            course_obj.description = dto.description
            course_obj.category = dto.category
            course_obj.level = dto.level

        Course.objects.bulk_update(course_objects,
                                   fields=["title", "description", "category",
                                           "level"])

        return [
            CourseDTO(
                course_id=obj.course_id,
                title=obj.title,
                description=obj.description,
                category=obj.category,
                level=obj.level,
                average_rating=obj.average_rating,
                estimated_duration=obj.estimated_duration_in_min,
            )
            for obj in course_objects
        ]

    def check_course_exists(self, course_id: str) -> bool:
        return Course.objects.filter(course_id=course_id).exists()

    def get_all_courses(self) -> list[CourseDTO]:
        courses = Course.objects.all()
        return [
            CourseDTO(
                course_id=course.course_id,
                title=course.title,
                description=course.description,
                category=course.category,
                level=course.level,
                average_rating=course.average_rating,
                estimated_duration=course.estimated_duration_in_min,
            )
            for course in courses
        ]

    def get_course_ids_by_title(self, titles: list[str]) -> list[str]:
        return list(Course.objects.filter(title__in=titles).
                    values_list('course_id', flat=True))

    def update_course_rating(self, course_id: str, rating: float) -> CourseDTO:
        course_data = Course.objects.get(course_id=course_id)
        course_data.average_rating = rating
        course_data.save()
        return CourseDTO(
            course_id=course_data.course_id,
            title=course_data.title,
            description=course_data.description,
            category=course_data.category,
            level=course_data.level,
            average_rating=course_data.average_rating,
            estimated_duration=course_data.estimated_duration_in_min,
        )
