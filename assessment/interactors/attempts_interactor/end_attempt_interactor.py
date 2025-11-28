"""End the attempt Interactor"""
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import AssessmentAttemptDTO, EndAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.dtos import StatusEnum
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.storages.topic_storage import TopicStorage


class EndAttemptInteractor(AssessmentValidationMixIn):
    """Create the end attempt interactor"""

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 assessment_storage: AssessmentStorageInterface,
                 enrollment_storage: EnrollmentStorageInterface,
                 topic_storage: TopicStorageInterface,
                 module_storage: ModuleStorageInterface):
        self.attempt_storage = attempt_storage
        self.assessment_storage = assessment_storage
        self.enrollment_storage = enrollment_storage
        self.topic_storage = topic_storage
        self.module_storage = module_storage


    def end_attempt(self, attempt_id: str) -> EndAttemptDTO:
        """End an attempt user click the end attempt """
        self.validate_attempt_exists(attempt_id=attempt_id,
                                     attempt_storage=self.attempt_storage)

        attempt_data = self.attempt_storage.get_assessment_attempt(
            attempt_id=attempt_id)

        assessment_data = self.assessment_storage.get_assessment(
            assessment_id=attempt_data.assessment_id)
        topic_id = assessment_data.topic_id
        topic = self.topic_storage.get_topics_by_topic_ids(topic_ids=[topic_id])[0]
        module_id = topic.module_id
        module = self.module_storage.get_modules(module_ids=[module_id])[0]
        course_id = module.course_id

        user_attempts = self.attempt_storage.get_user_assessment_attempts(
            user_id=attempt_data.user_id,
            assessment_id=assessment_data.assessment_id)

        if assessment_data.attempts_limit == len(user_attempts):

            check_fails = [attempt.total_points for attempt in user_attempts if int(attempt.total_points) >= assessment_data.pass_marks ]

            if not check_fails:
                self.enrollment_storage.update_enrollment_status(user_id=user_attempts[0].user_id,course_id=course_id)



        return self.attempt_storage.end_an_attempt(attempt_id=attempt_id,
                                                   status=StatusEnum.COMPLETE)
