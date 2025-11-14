from abc import ABC, abstractmethod

from assessment.interactors.dtos import \
    UserQuestionSubmittedDTO


class AttemptSubmittedQuestionStorageInterface(ABC):

    @abstractmethod
    def get_answered_submission_questions(self, attempt_id: str) -> list[str]:
        pass

    @abstractmethod
    def create_attempted_question(self,
                                  assessment_submission_details: UserQuestionSubmittedDTO) \
            -> UserQuestionSubmittedDTO:
        pass

    @abstractmethod
    def get_attempt_questions(self, attempt_ids: list[str])->list[str]:
        pass