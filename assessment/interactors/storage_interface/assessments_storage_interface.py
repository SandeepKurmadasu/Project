from abc import ABC, abstractmethod

from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO, CreateAssessmentDBDTO


class AssessmentStorageInterface(ABC):

    @abstractmethod
    def assessment_exists(self, assessment_id: str) -> bool:
        pass

    @abstractmethod
    def create_assessments(self, assessments: list[CreateAssessmentDBDTO]) -> \
            list[AssessmentDTO]:
        pass

    @abstractmethod
    def get_assessment(self, assessment_id: str) -> AssessmentDTO:
        pass

    @abstractmethod
    def update_marks_in_assessment(self, assessment_id: str, marks: int,
                                   pass_marks: int) -> AssessmentDTO:
        pass

    @abstractmethod
    def get_assessment_by_topic_id(self, topic_id: str) -> AssessmentDTO:
        pass