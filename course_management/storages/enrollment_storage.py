from course_management.interactors.dtos import EnrollmentDTO, CourseDTO
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface


class EnrollmentStorage(EnrollmentStorageInterface):

    def get_user_course_enrollment_exist(self, course_id: str,user_id : str) -> bool:
        pass

    def get_user_enrolled_courses(self, user_id: str) -> list[str]:
        pass

    def create_enrollment(self,user_id: str, course_id : str)->EnrollmentDTO:
        pass

    def update_course_percentage(self,user_id : str, course_id : str)->EnrollmentDTO:
        pass