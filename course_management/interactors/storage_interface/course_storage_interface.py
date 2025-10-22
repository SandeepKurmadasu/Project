import abc

from course_management.interactors.storage_interface.dtos import UserDTO
from course_management.interactors.storage_interface.dtos import CourseDTO, TopicProgressDTO
from course_management.interactors.storage_interface.dtos import CreateCourseRequestDTO, UpdateCourseRequestDTO,CourseRecommendationDTO
from typing import List

class CourseStorageInterface(abc.ABC):

    @abc.abstractmethod
    def get_courses_by_ids(self,course_ids : List[str]) -> List[CourseDTO]:
        pass

    @abc.abstractmethod
    def bulk_create_courses(self,courses: List[CreateCourseRequestDTO]) -> List[CourseDTO]:
        pass

    @abc.abstractmethod
    def bulk_update_courses(self,course_ids:List[UpdateCourseRequestDTO]) -> List[CourseDTO]:
        pass

    @abc.abstractmethod
    def get_courses_by_category(self, category: str, limit: int) -> List[CourseDTO]:
        pass

    @abc.abstractmethod
    def get_user_by_id(self,user_id: str)->UserDTO:
        pass

    @abc.abstractmethod
    def get_total_course_hours(self, course_id: str) -> float:
        pass



class ProgressStorageInterface(abc.ABC):

    @abc.abstractmethod
    def get_course_progress(self,user_id: str,course_id: str):
        pass

    @abc.abstractmethod
    def get_all_topics_progress(self,user_id: str,course_id: str) ->List[TopicProgressDTO]:
        pass

    @abc.abstractmethod
    def get_next_incomplete_topic(self, user_id: str, course_id: str) -> str:
        pass





