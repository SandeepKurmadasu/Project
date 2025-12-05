from course_management.interactors.dtos import \
    CourseFeedbackDTO
from course_management.interactors.storage_interfaces.course_feedback_storage_interface import \
    CourseFeedbackStorageInterface
from course_management.models import User, Course
from course_management.models.models import CourseFeedback


class FeedbackStorage(CourseFeedbackStorageInterface):

    def get_course_rating(self, course_id: str) -> list[CourseFeedbackDTO]:
        feedbacks = CourseFeedback.objects.filter(course_id=course_id)

        return [
            CourseFeedbackDTO(
                user_id=each_course_feedback.user.user_id,
                course_id=each_course_feedback.course.course_id,
                rating=each_course_feedback.rating,
                message=each_course_feedback.message
            ) for each_course_feedback in feedbacks
        ]

    def create_course_feedback(self,
                               feedback: CourseFeedbackDTO) -> CourseFeedbackDTO:
        user = User.objects.get(user_id=feedback.user_id)
        course = Course.objects.get(course_id=feedback.course_id)

        created_data = CourseFeedback.objects.create(user=user, course=course,
                                                     rating=feedback.rating,
                                                     message=feedback.message)

        return CourseFeedbackDTO(
            user_id=created_data.user.user_id,
            course_id=created_data.course.course_id,
            rating=created_data.rating,
            message=created_data.message
        )

    def check_already_feedback_exists(self, user_id: str,
                                      course_id: str) -> bool:
        return CourseFeedback.objects.filter(user_id=user_id,
                                             course_id=course_id).exists()
