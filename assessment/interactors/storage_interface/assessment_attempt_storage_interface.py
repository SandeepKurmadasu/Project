from abc import ABC, abstractmethod

from assessment.interactors.dtos import AssessmentAttemptDTO, \
    AssessmentAttemptProgressDTO, QuestionDTO
from course_management.interactors.dtos import StatusEnum


class AttemptStorageInterface(ABC):

    @abstractmethod
    def create_assessment_attempt(self, user_id: str,
                                  assessment_id: str) -> AssessmentAttemptDTO:
        pass

    @abstractmethod
    def get_latest_assessment_attempt(self, user_id: str,
                                      assessment_id: str) -> AssessmentAttemptDTO:
        pass

    @abstractmethod
    def get_assessment_attempt(self, attempt_id: str) -> AssessmentAttemptDTO:
        pass

    @abstractmethod
    def get_assessment_progress(self,
                                attempt_id: str) -> AssessmentAttemptProgressDTO:
        pass

    @abstractmethod
    def check_attempt_exist(self, attempt_id: str) -> bool:
        pass

    @abstractmethod
    def complete_assessment_attempt(self,
                                    attempt_id: str) -> AssessmentAttemptProgressDTO:
        pass

    @abstractmethod
    def update_assessment_total_points(self, attempt_id: str,
                                       points: float) -> AssessmentAttemptDTO:
        pass

    @abstractmethod
    def end_an_attempt(self, attempt_id: str,
                       status: StatusEnum.COMPLETE) -> AssessmentAttemptDTO:
        pass
