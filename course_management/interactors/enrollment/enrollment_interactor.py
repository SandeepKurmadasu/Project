from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import EnrollmentDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface
from typing import List

class EnrollmentInteractor(ValidationMixIns):

    def __init__(self,enrollment_storage: EnrollmentStorageInterface,user_storage: UserStorageInterface,course_storage: CourseStorageInterface):
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage
        self.course_storage = course_storage

    def enroll_user_in_course(self,user_id: str, course_id: str)->EnrollmentDTO:
        self.check_if_user_exists(user_id=user_id,user_storage=self.user_storage)
        self.check_if_course_exists(course_id=course_id,course_storage=self.course_storage)

        return self.enrollment_storage.create_enrollment(user_id=user_id,course_id=course_id)

    def get_user_enrolled_courses(self, user_id: str)->List[EnrollmentDTO]:
        self.check_if_user_exists(user_id=user_id,user_storage=self.user_storage)

        return self.enrollment_storage.get_user_enrollments(user_id=user_id)

