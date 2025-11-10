from abc import ABC, abstractmethod

from course_management.interactors.dtos import \
    UnitLearningProgressDTO, \
    UserLearningUnitProgressDTO, \
    UpdateLearningUnitProgressResponseDTO, UpdateLearningUnitProgressDTO, \
    LearningUnitDTO


class UserLearningUnitStorageInterface(ABC):

    @abstractmethod
    def get_all_user_learning_unit_progress(self,
                                            user_learning_path_id: str) -> \
            list[UnitLearningProgressDTO]:
        pass

    @abstractmethod
    def get_user_learning_unit_progress(self, user_learning_path_id: str,
                                        learning_unit_id: str) -> UserLearningUnitProgressDTO:
        pass

    @abstractmethod
    def update_learning_unit_progress(self,update_data: UpdateLearningUnitProgressDTO) \
            -> UnitLearningProgressDTO:
        pass

    @abstractmethod
    def get_next_learning_unit(self, user_learning_path_id: str,
                               current_order: int) -> LearningUnitDTO:
        pass

    @abstractmethod
    def unlock_learning_unit(self, user_learning_path_id: str,
                             learning_unit_id: str) -> UserLearningUnitProgressDTO:
        pass

    @abstractmethod
    def get_learning_units_by_topic_ids(self, user_id: str,
                                        topic_ids: list[str]) -> list[
        UnitLearningProgressDTO]:
        pass
