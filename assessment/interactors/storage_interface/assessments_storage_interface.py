from abc import ABC, abstractmethod

from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO


class AssessmentStorageInterface(ABC):

    @abstractmethod
    def assessment_exists(self, assessment_id: str) -> bool:
        pass

    @abstractmethod
    def create_assessments(self, assessments: list[CreateAssessmentDTO]) -> \
            list[AssessmentDTO]:
        pass

    @abstractmethod
    def get_assessment(self, assessment_id: str) -> AssessmentDTO:
        pass
