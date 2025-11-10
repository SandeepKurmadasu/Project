from abc import ABC, abstractmethod

from course_management.interactors.dtos import \
    UserLearningPathDTO


class UserLearningPathStorageInterface(ABC):

    @abstractmethod
    def get_user_learning_path(self, user_id: str,
                               course_id: str) -> UserLearningPathDTO:
        pass

    @abstractmethod
    def get_user_learning_path_with_id(self, user_id: str,
                                       learning_path_id: str):
        pass

    @abstractmethod
    def create_user_learning_path(self, user_id: str,
                                  course_learning_path_id: str) -> UserLearningPathDTO:
        pass

    @abstractmethod
    def get_user_learning_path_with_user_learning_path_id(self,
                                                          user_learning_path_id: str) -> UserLearningPathDTO:
        pass

    @abstractmethod
    def check_user_learning_path_exists(self,
                                        user_learning_path_id: str) -> bool:
        pass

    @abstractmethod
    def update_user_learning_path_percentage(self, user_learning_path_id: str,
                                             percentage: int) -> UserLearningPathDTO:
        pass
