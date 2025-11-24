from abc import ABC, abstractmethod

from course_management.interactors.dtos import \
    LearningUnitProgressDTO, UserLearningUnitProgressDTO, \
    UpdateLearningUnitProgressDTO, LearningUnitDTO, UserLearningUnitDTO, \
    CreateUserLearningUnit


class UserLearningUnitStorageInterface(ABC):

    @abstractmethod
    def create_user_learning_units(self, user_learning_units: list[
        CreateUserLearningUnit]) -> list[UserLearningUnitDTO]:
        pass

    @abstractmethod
    def get_all_user_learning_unit_progress(self,
                                            user_learning_path_id: str) -> \
            list[LearningUnitProgressDTO]:
        pass

    @abstractmethod
    def get_user_learning_unit_progress(self, user_learning_path_id: str,
                                        learning_unit_id: str) -> UserLearningUnitProgressDTO:
        pass

    @abstractmethod
    def update_learning_unit_progress(self,
                                      update_data: UpdateLearningUnitProgressDTO) \
            -> LearningUnitProgressDTO:
        pass

    @abstractmethod
    def get_next_learning_unit(self, user_learning_path_id: str,
                               current_order: int) -> UserLearningUnitDTO:
        pass

    @abstractmethod
    def unlock_learning_unit(self, user_learning_path_id: str,
                             user_learning_unit_id: int) -> UserLearningUnitProgressDTO:
        pass

    @abstractmethod
    def get_learning_units_by_topic_ids(
            self, user_id: str, topic_ids: list[str]) -> list[
        LearningUnitProgressDTO]:
        pass

    @abstractmethod
    def get_user_learning_unit_by_id(self,
                                     user_learning_unit_id: int) -> UserLearningUnitDTO:
        pass

    @abstractmethod
    def get_user_learning_unit_progress_by_id(self,
                                              user_learning_unit_id: int) -> UserLearningUnitProgressDTO |None:
        pass
