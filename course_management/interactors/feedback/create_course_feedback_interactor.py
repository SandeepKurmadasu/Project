from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    CourseFeedbackDTO, CourseDTO
from course_management.interactors.storage_interfaces.course_feedback_storage_interface import \
    CourseFeedbackStorageInterface
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class CreateCourseFeedbackInteractor(ValidationMixIn):
    def __init__(self, feedback_storage: CourseFeedbackStorageInterface,
                 course_storage: CourseStorageInterface,
                 user_storage: UserStorageInterface):
        self.course_storage = course_storage
        self.feedback_storage = feedback_storage
        self.user_storage = user_storage

    def create_course_feedback(self,
                               feedback_data: CourseFeedbackDTO) -> CourseFeedbackDTO:
        self.check_course_exists(course_id=feedback_data.course_id,
                                 course_storage=self.course_storage)
        self.check_user_exists(user_id=feedback_data.user_id,
                               user_storage=self.user_storage)
        feedback = self.feedback_storage.create_course_feedback(
            feedback=feedback_data)

        self._update_course_rating(course_id=feedback_data.course_id)
        return feedback

    def _update_course_rating(self, course_id: str) -> CourseDTO:
        course_feedbacks = self.feedback_storage.get_course_rating(
            course_id=course_id)
        rating = sum([obj.rating for obj in course_feedbacks]) / len(
            course_feedbacks)

        return self.course_storage.update_course_rating(course_id=course_id,
                                                        rating=rating)
