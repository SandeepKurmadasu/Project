# pylint: disable=too-few-public-methods
"""Create the automatic attempt end interactor"""
import datetime

from assessment.interactors.attempts_interactor.end_attempt_interactor import \
    EndAttemptInteractor
from assessment.interactors.dtos import  EndAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.storage_interfaces.enrollment_storage_interface import \
    EnrollmentStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import TopicStorageInterface


class AttemptAutoEndInteractor:
    """ Auto end attempt based on time out interactor """

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 assessment_storage: AssessmentStorageInterface,
                 enrollment_storage: EnrollmentStorageInterface,
                 topic_storage: TopicStorageInterface,
                 module_storage: ModuleStorageInterface,
                 ):
        self.attempt_storage = attempt_storage
        self.assessment_storage = assessment_storage
        self.enrollment_storage = enrollment_storage
        self.topic_storage = topic_storage
        self.module_storage = module_storage


    def auto_end_attempt(self, attempt_id: str) -> EndAttemptDTO | None:
        """ Automatically end the assessment attempt with time period """
        now = datetime.datetime.now(datetime.timezone.utc)

        attempt_data = self.attempt_storage.get_assessment_attempt(
            attempt_id=attempt_id)

        assessment_data = self.assessment_storage.get_assessment(
            assessment_id=attempt_data.assessment_id)

        expiry_time = attempt_data.started_at + datetime.timedelta(
            minutes=assessment_data.estimate_duration_in_mins)

        if now >= expiry_time:
            interactor = EndAttemptInteractor(
                attempt_storage=self.attempt_storage,
                assessment_storage=self.assessment_storage,
                enrollment_storage=self.enrollment_storage,
                topic_storage=self.topic_storage,
                module_storage=self.module_storage,
            )
            result = interactor.end_attempt(attempt_id=attempt_id)
            return result

        return None
