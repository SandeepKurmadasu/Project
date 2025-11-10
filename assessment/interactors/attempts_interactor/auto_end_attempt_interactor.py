# pylint: disable=too-few-public-methods
"""Create the automatic attempt end interactor"""
import datetime

from assessment.interactors.dtos import AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.dtos import StatusEnum


class AttemptAutoEndInteractor:
    """ Auto end attempt based on time out interactor """

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 assessment_storage: AssessmentStorageInterface):
        self.attempt_storage = attempt_storage
        self.assessment_storage = assessment_storage

    def auto_end_attempt(self, attempt_id: str) -> AssessmentAttemptDTO | None:
        """ Automatically end the assessment attempt with time period """
        now = datetime.datetime.now()

        attempt_data = self.attempt_storage.get_assessment_attempt(
            attempt_id=attempt_id)

        assessment_data = self.assessment_storage.get_assessment(
            assessment_id=attempt_data.assessment_id)

        expiry_time = attempt_data.started_at + datetime.timedelta(
            minutes=assessment_data.estimate_duration_in_mins)

        if now >= expiry_time:
            result = self.attempt_storage.end_an_attempt(attempt_id=attempt_id,
                                                         status=StatusEnum.COMPLETE)
            return result

        return None
