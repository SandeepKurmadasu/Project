from course_management.interactors.dtos import CourseDTO, CreateCourseDTO, UpdateCourseDTO, ModuleDTO, TopicDTO, UserTopicCompletionPercentageDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface

class CourseStorage(CourseStorageInterface):

    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        pass

    def get_valid_course_ids(self, course_ids: list[str]) -> list[str]:
        pass

    def create_courses(self, courses: list[CreateCourseDTO]) -> list[CourseDTO]:
        pass

    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[CourseDTO]:
        pass

    def check_course_exists(self, course_id: str) -> bool:
        pass

    def get_recommend_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        pass

    def get_all_course_ids(self) -> list[str]:
        pass

    def get_excluded_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        pass

    def get_topics_in_course(self, course_id: str):
        pass

    def get_title_course_ids(self, titles: list[str]) -> list[str]:
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