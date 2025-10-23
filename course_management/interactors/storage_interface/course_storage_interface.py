from abc import ABC, abstractmethod
from course_management.interactors.dtos import CourseDTO,CreateCourseDTO, UpdateCourseDTO,ModuleDTO,TopicDTO,UserTopicCompletionPercentageDTO

class CourseStorageInterface(ABC):

    @abstractmethod
    def get_courses(self,course_ids : list[str])->list[CourseDTO]:
        pass

    @abstractmethod
    def get_valid_course_ids(self,course_ids : list[str])->list[str]:
        pass

    @abstractmethod
    def create_courses(self, courses : list[CreateCourseDTO])->list[CourseDTO]:
        pass

    @abstractmethod
    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[CourseDTO]:
        pass

    @abstractmethod
    def check_course_exists(self,course_id : str)->bool:
        pass

    @abstractmethod
    def get_recommend_courses(self,course_ids : list[str])->list[CourseDTO]:
        pass

    @abstractmethod
    def get_topics_in_course(self,course_id :str):
        pass

    @abstractmethod
    def get_title_course_ids(self,titles : list[str])->list[str]:
        pass

    @abstractmethod
    def get_enum_types(self)->list[str]:
        pass

    @abstractmethod
    def get_modules_in_course(self, course_id: str) -> list[ModuleDTO]:
        pass

    @abstractmethod
    def get_topics_in_module(self, module_id: str) -> list[TopicDTO]:
        pass

    @abstractmethod
    def get_user_topic_completion_percentages(self, user_id: str, topic_ids: list[str]) -> list[UserTopicCompletionPercentageDTO]:
        pass

    @abstractmethod
    def get_topics_for_modules(self, module_ids: list[str]) -> list[TopicDTO]:
        pass

    @abstractmethod
    def get_topics_in_modules(self, module_ids: list[str]) -> list[TopicDTO]:
        pass

