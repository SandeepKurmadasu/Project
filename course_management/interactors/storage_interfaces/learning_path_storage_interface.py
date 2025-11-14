from abc import ABC, abstractmethod

from course_management.interactors.dtos import LearningPathForCourseDTO


class LearningPathStorageInterface(ABC):

    @abstractmethod
    def create_course_learning_path(self,
                                    course_id: str) -> LearningPathForCourseDTO:
        pass

    @abstractmethod
    def get_course_learning_path(self,
                                 learning_path_id: str) -> LearningPathForCourseDTO:
        pass

    @abstractmethod
    def learning_path_exist(self, learning_path_id: str) -> bool:
        pass

    @abstractmethod
    def get_latest_learning_path_by_course_id(self,
                                              course_id: str) -> LearningPathForCourseDTO:
        pass

