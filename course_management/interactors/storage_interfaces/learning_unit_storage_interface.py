from abc import ABC, abstractmethod

from course_management.interactors.dtos import LearningUnitDTO, \
    CreateLearningUnitDTO


class LearningUnitStorageInterface(ABC):

    @abstractmethod
    def check_learning_unit_exists(self, learning_unit_id: str) -> bool:
        pass

    @abstractmethod
    def get_learning_unit(self, learning_unit_id: str) -> LearningUnitDTO:
        pass


    @abstractmethod
    def create_learning_units(self,
                              learning_units: list[CreateLearningUnitDTO]) -> \
            list[LearningUnitDTO]:
        pass

    @abstractmethod
    def get_learning_units_by_learning_path_id(self, learning_path_id: str) -> \
            list[LearningUnitDTO]:
        pass
