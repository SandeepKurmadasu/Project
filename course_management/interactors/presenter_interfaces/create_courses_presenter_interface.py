from abc import ABC, abstractmethod
from typing import Any

from course_management.interactors.dtos import CourseDTO


class CreateCoursesPresenterInterface(ABC):

    @abstractmethod
    def present_courses(self, courses: list[CourseDTO]) -> Any:
        pass
