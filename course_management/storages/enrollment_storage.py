from course_management.interactors.dtos import EnrollmentDTO
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.models import Enrollment

class EnrollmentStorage(EnrollmentStorageInterface):

    def get_user_enrolled_courses(self, user_id: str) -> list[str]:
        return list(
            Enrollment.objects.filter(user_id=user_id).values_list('course_id',flat=True)
        )

    def create_enrollment(self,user_id: str, course_id : str)->EnrollmentDTO:
        enrollment=Enrollment.objects.create(
            user_id=user_id,
            course_id=course_id,
            course_percentage=0

        )
        return EnrollmentDTO(
            id=enrollment.id,
            user_id=enrollment.user.user_id,
            course_id=enrollment.course.course_id,
            course_percentage=enrollment.course_percentage
        )

    def update_course_percentage(self,user_id : str, course_id : str,percentage: int)->EnrollmentDTO:
        enrollment=Enrollment.objects.get(user_id=user_id,course_id=course_id)
        enrollment.course_percentage=percentage
        enrollment.save()

        return EnrollmentDTO(
            id=enrollment.id,
            user_id=enrollment.user.user_id,
            course_id=enrollment.course.course_id,
            course_percentage=enrollment.course_percentage
        )

    def get_user_enrollments(self, user_id: str) ->list[EnrollmentDTO]:
        enrollment_objects=Enrollment.objects.filter(user_id=user_id)
        enrollment_dtos=[]
        for e in enrollment_objects:
            enrollment_dtos.append(
                EnrollmentDTO(
                    id=e.id,
                    user_id=e.user.user_id,
                    course_id=e.course.course_id,
                    course_percentage=e.course_percentage
                )
            )
        return enrollment_dtos


    def get_user_course_enrollment_exist(self, course_id: str,user_id : str) -> bool:
        pass
