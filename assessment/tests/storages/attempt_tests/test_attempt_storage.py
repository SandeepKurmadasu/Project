import datetime

import pytest

from assessment.storages.attempt_storage import AttemptStorage
from assessment.tests.factories.storage_factories import AssessmentFactory, \
    AttemptFactory
from course_management.tests.factories.storage_factories import UserFactory


class TestAttempt:

    @pytest.mark.django_db
    def test_create_assessment_attempt(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"

        UserFactory(user_id=user_id)
        AssessmentFactory(assessment_id=assessment_id)
        attempt_storage = AttemptStorage()
        question_ids = ["12345678-1234-5678-1234-567812345681",
                        "12345678-1234-5678-1234-567812345680"]

        result = attempt_storage.create_assessment_attempt(user_id=user_id,
                                                           assessment_id=assessment_id,
                                                           question_ids=question_ids)

        output = f"{result.user_id} - {result.assessment_id}"
        snapshot.assert_match(repr(output),
                              "test_create_assessment_attempt.txt")



    @pytest.mark.django_db
    def test_get_latest_assessment_attempt(self, snapshot):
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51,
                                                  922886)
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        attempt_storage = AttemptStorage()
        question_ids = ["12345678-1234-5678-1234-567812345681",
                        "12345678-1234-5678-1234-567812345680"]

        AttemptFactory(attempt_id=attempt_id,user=user,assessment=assessment,question_ids=question_ids,started_at=start_time)

        result = attempt_storage.get_latest_assessment_attempt(user_id=user_id,
                                                           assessment_id=assessment_id)

        snapshot.assert_match(repr(result),
                              "test_create_assessment_attempt.txt")


