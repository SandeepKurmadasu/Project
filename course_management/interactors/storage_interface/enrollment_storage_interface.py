from abc import ABC, abstractmethod

from course_management.interactors.dtos import EnrollmentDTO


class EnrollmentStorageInterface(ABC):

    @abstractmethod
    def get_user_course_enrollment_exist(self, course_id: str, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_enrolled_courses(self, user_id: str) -> list[EnrollmentDTO]:
        pass

    @abstractmethod
    def create_enrollment(self, user_id: str, course_id: str) -> EnrollmentDTO:
        pass

    @abstractmethod
    def update_course_percentage(self,user_id : str, course_id : str)->EnrollmentDTO:
        pass