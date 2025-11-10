from abc import ABC, abstractmethod

from course_management.interactors.dtos import \
    CourseFeedbackDTO


class CourseFeedbackStorageInterface(ABC):

    @abstractmethod
    def get_course_rating(self, course_id: str) -> list[CourseFeedbackDTO]:
        pass

    @abstractmethod
    def create_course_feedback(self,
                               feedback: CourseFeedbackDTO) -> CourseFeedbackDTO:
        pass
