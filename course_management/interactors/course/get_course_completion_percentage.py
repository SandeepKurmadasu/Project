from course_management.exceptions.custom_exceptions import UserNotEnrolledCourse
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import CoursePercentageDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface
from course_management.interactors.course.course_completion_calculation import CourseCompletionCalculator

class UserCoursesCompletionPercentageInteractor(ValidationMixIns):

    def __init__(self,course_storage: CourseStorageInterface,enrollment_storage: EnrollmentStorageInterface,user_storage: UserStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage

    def get_user_course_completion_percentage(self, user_id: str, course_id: str) -> CoursePercentageDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_if_course_exists(course_id=course_id, course_storage=self.course_storage)
        self._check_user_course_enrollment(user_id=user_id, course_id=course_id)

        # GET MODULES IN THE COURSE
        modules = self.course_storage.get_modules_in_course(course_id)
        if not modules:
            return CoursePercentageDTO(user_id=user_id, course_id=course_id, percentage=0)
        module_ids = [module.module_id for module in modules]

        #GET TOPICS IN MODULES
        topics = self.course_storage.get_topics_in_modules(module_ids)
        if not topics:
            return CoursePercentageDTO(user_id=user_id, course_id=course_id, percentage=0)

        all_topic_ids = [topic.topic_id for topic in topics]

        #GET USER TOPIC COMPLETION PERCENTAGES
        user_topic_progress = self.course_storage.get_user_topic_completion_percentages(
            user_id=user_id, topic_ids=all_topic_ids
        )

        course_percentage = CourseCompletionCalculator.calculate_course_percentage(
            modules=modules,
            topics=topics,
            user_topic_progress=user_topic_progress
        )

        return CoursePercentageDTO(
            user_id=user_id,
            course_id=course_id,
            percentage=int(course_percentage)
        )

    def _check_user_course_enrollment(self, user_id: str, course_id: str):
        is_user_enrolled = self.enrollment_storage.get_user_course_enrollment_exist(
            course_id=course_id, user_id=user_id
        )
        if not is_user_enrolled:
            raise UserNotEnrolledCourse(user_id=user_id)