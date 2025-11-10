from course_management.interactors.dtos import EnrollmentDTO
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.models import Enrollment, User, Course


class EnrollmentStorage(EnrollmentStorageInterface):

    def check_user_course_enrollment_exist(self, course_id: str,
                                           user_id: str) -> bool:
        return Enrollment.objects.filter(user_id=user_id,
                                         course_id=course_id).exists()

    def get_user_enrolled_courses(self, user_id: str) -> list[EnrollmentDTO]:
        user_enrollments = Enrollment.objects.filter(user_id=user_id)

        get_user_enrollments = [EnrollmentDTO(
            id=each_enroll.pk,
            user_id=each_enroll.user.user_id,
            course_id=each_enroll.course.course_id,
            course_status=each_enroll.course_status,
            course_percentage=each_enroll.course_percentage
        ) for each_enroll in user_enrollments]

        return get_user_enrollments

    def create_enrollment(self, user_id: str, course_id: str) -> EnrollmentDTO:
        user = User.objects.get(user_id=user_id)
        course = Course.objects.get(course_id=course_id)
        enrollment = Enrollment.objects.create(user=user, course=course)

        return EnrollmentDTO(
            id=enrollment.pk,
            user_id=enrollment.user.user_id,
            course_id=enrollment.course.course_id,
            course_status=enrollment.course_status,
            course_percentage=enrollment.course_percentage
        )

    def update_course_percentage(self, user_id: str, course_id: str,
                                 percentage: int) -> EnrollmentDTO:
        user_course = Enrollment.objects.get(user=user_id, course=course_id)
        user_course.course_percentage = percentage
        user_course.save()

        return EnrollmentDTO(
            id=user_course.pk,
            user_id=user_course.user.user_id,
            course_id=user_course.course.course_id,
            course_status=user_course.course_status,
            course_percentage=user_course.course_percentage
        )

    def get_enrollment(self, user_id: str, course_id: str) -> EnrollmentDTO:
        user_course = Enrollment.objects.get(user=user_id, course=course_id)

        return EnrollmentDTO(
            id=user_course.pk,
            user_id=user_course.user.user_id,
            course_id=user_course.course.course_id,
            course_status=user_course.course_status,
            course_percentage=user_course.course_percentage
        )
