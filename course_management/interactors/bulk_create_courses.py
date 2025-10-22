from course_management.interactors.storage_interface.dtos import CreateCourseRequestDTO, CourseDTO, CourseValidator
from course_management.interactors.storage_interface.course_storage_interface import CreateCourseInterface
from typing import List

class CreateCourseInteractor:

    def __init__(self,course_storage:CreateCourseInterface):
        self.course_storage=course_storage

    def bulk_create_courses(self,requests : List[CreateCourseRequestDTO]) -> List[CourseDTO]:
        CourseValidator.validate_bulk_course_data(requests)
        courses=self.course_storage.bulk_create_courses(courses=requests)
        return courses
