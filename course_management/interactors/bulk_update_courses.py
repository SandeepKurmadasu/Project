from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface, UpdateCourseRequestDTO, CourseDTO
from course_management.validations.course_validations import CourseValidator
from typing import List
from course_management.exceptions.course_exceptions import InvalidCourseIds

class BulkUpdateInteractor:
    def __init__(self,course_storage:CourseStorageInterface):
        self.course_storage=course_storage

    def bulk_update_courses(self,requests :List[UpdateCourseRequestDTO]) -> List[CourseDTO]:
        CourseValidator.validate_bulk_course_data(requests)
        courses = self.course_storage.bulk_update_courses(courses=requests)
        return courses