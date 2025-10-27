from course_management.exceptions.custom_exceptions import UserNotEnrolledCourse
from course_management.interactors.storage_interface.module_storage_interface import ModuleStorageInterface
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import CoursePercentageDTO
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.enrollment_storage_interface import EnrollmentStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface

class GetCourseCompletionPercentageInteractor(ValidationMixIns):

    def __init__(self,course_storage: CourseStorageInterface,enrollment_storage: EnrollmentStorageInterface,user_storage: UserStorageInterface,module_storage: ModuleStorageInterface,topic_storage: TopicStorageInterface):
        self.course_storage = course_storage
        self.enrollment_storage = enrollment_storage
        self.user_storage = user_storage
        self.module_storage=module_storage
        self.topic_storage=topic_storage


    def get_course_completion_percentage(self, user_id: str, course_id: str) -> CoursePercentageDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.check_if_course_exists(course_id=course_id, course_storage=self.course_storage)
        self._check_user_course_enrollment(user_id=user_id, course_id=course_id)

        course_completion_percentage = self.calculate_user_course_completion_percentage(course_id=course_id,
                                                                                        user_id=user_id)
        self.enrollment_storage.update_course_percentage(user_id=user_id, course_id=course_id,
                                                         course_percentage=course_completion_percentage)

        return CoursePercentageDTO(
            user_id=user_id,
            course_id=course_id,
            percentage=course_completion_percentage
        )

    def _check_user_course_enrollment(self, user_id: str, course_id: str):
        is_user_enrolled = self.enrollment_storage.get_user_course_enrollment_exist(course_id=course_id,
                                                                                      user_id=user_id)

        if not is_user_enrolled:
            raise UserNotEnrolledCourse(user_id=user_id)

    def calculate_user_course_completion_percentage(self, course_id: str, user_id: str) -> int:
        course_modules = self.module_storage.get_course_modules(course_id=course_id)
        module_ids = [obj.module_id for obj in course_modules]
        topics = self.topic_storage.get_topics_for_module_ids(module_ids=module_ids)
        topic_ids = [obj.topic_id for obj in topics]

        topic_percentages = self.topic_storage.get_user_topic_progresses(user_id=user_id, topic_ids=topic_ids)
        if not topic_percentages:
            return 0

        total_topics_percentage = sum([obj.percentage for obj in topic_percentages])

        course_completion_percentage = int(total_topics_percentage / len(topic_ids))

        return course_completion_percentage