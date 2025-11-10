from abc import ABC, abstractmethod

from course_management.interactors.dtos import CourseDTO, \
    CreateCourseDTO, UpdateCourseDTO


class CourseStorageInterface(ABC):

    @abstractmethod
    def get_courses(self, course_ids: list[str]) -> list[CourseDTO]:
        pass

    @abstractmethod
    def get_valid_course_ids(self, course_ids: list[str]) -> list[str]:
        pass

    @abstractmethod
    def create_courses(self, courses: list[CreateCourseDTO]) -> list[
        CourseDTO]:
        pass

    @abstractmethod
    def update_courses(self, courses: list[UpdateCourseDTO]) -> list[
        CourseDTO]:
        pass

    @abstractmethod
    def check_course_exists(self, course_id: str) -> bool:
        pass

    @abstractmethod
    def get_all_courses(self):
        pass

    @abstractmethod
    def get_course_ids_by_title(self, titles: list[str]) -> list[str]:
        pass

    @abstractmethod
    def update_course_rating(self, course_id: str, rating: float) -> CourseDTO:
        pass
