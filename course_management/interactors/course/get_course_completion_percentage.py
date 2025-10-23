from course_management.exceptions.custom_exceptions import UserNotEnrolledCourse
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import CoursePercentageDTO, UserTopicCompletionPercentageDTO, ModuleDTO, TopicDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface
class UserCoursesCompletionPercentageInteractor(ValidationMixIns):

    def __init__(
        self,
        course_storage: CourseStorageInterface,
        enrollment_storage: EnrollmentStorageInterface,
        user_storage: UserStorageInterface
    ):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage

    def get_user_course_completion_percentage(self, user_id: str, course_id: str) -> CoursePercentageDTO:
        # Step 1: Validations
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_if_course_exists(course_id=course_id, course_storage=self.course_storage)
        self._check_user_course_enrollment(user_id=user_id, course_id=course_id)

        # Step 2: Get all modules in the course
        modules: list[ModuleDTO] = self.course_storage.get_modules_in_course(course_id)
        if not modules:
            return CoursePercentageDTO(user_id=user_id, course_id=course_id, percentage=0)

        module_percentages = []

        # Step 3 & 4: Loop through each module and fetch user topic completion
        for module in modules:
            topics: list[TopicDTO] = self.course_storage.get_topics_in_module(module.module_id)

            if not topics:
                module_percentages.append(0)
                continue

            topic_ids = [topic.topic_id for topic in topics]

            # Fetch user topic completion percentages
            user_topic_progress: list[UserTopicCompletionPercentageDTO] = \
                self.course_storage.get_user_topic_completion_percentages(user_id=user_id, topic_ids=topic_ids)

            if not user_topic_progress:
                module_percentages.append(0)
            else:
                # Step 5: Calculate module average completion
                module_avg = sum([t.percentage for t in user_topic_progress]) / len(user_topic_progress)
                module_percentages.append(module_avg)

        # Step 6: Calculate overall course completion
        course_percentage = sum(module_percentages) / len(module_percentages) if module_percentages else 0

        # Return result DTO
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
