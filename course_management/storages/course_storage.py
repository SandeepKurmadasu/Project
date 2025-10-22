from course_management.interactors.dtos import CourseDTO, CreateCourseDTO, UpdateCourseDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface


class CourseStorage(CourseStorageInterface):

    def get_courses(self,course_ids : list[str]) ->list[CourseDTO]:
        pass

    def get_valid_course_ids(self,course_ids : list[str])->list[str]:
        # Get all given course ids if exists
        pass

    def create_courses(self, courses : list[CreateCourseDTO])->list[CourseDTO]:
        # Create courses
        pass

    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[CourseDTO]:
        pass

    def check_course_exists(self,course_id : str)->bool:
        pass

    def get_excluded_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        # Course.objects.exclude(course_id__in=courseId)
        pass

    def get_topics_in_course(self,course_id :str):
        pass

    def get_title_course_ids(self,titles : list[str])->list[str]:
        pass

    def get_enum_types(self)->list[str]:
        # unique_types = Course.objects.values(types).distinct()
        pass