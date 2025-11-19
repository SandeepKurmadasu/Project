import datetime
from decimal import Decimal

import pytest
from freezegun import freeze_time

from assessment.storages.attempt_storage import AttemptStorage
from assessment.tests.factories.storage_factories import AssessmentFactory, \
    AttemptFactory
from course_management.interactors.dtos import StatusEnum
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
    @freeze_time("2025-11-18 13:21:51.922886")
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

        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       question_ids=question_ids, started_at=start_time)

        result = attempt_storage.get_latest_assessment_attempt(user_id=user_id,
                                                               assessment_id=assessment_id)

        snapshot.assert_match(repr(result),
                              "test_create_assessment_attempt.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_get_assessment_attempted_questions(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        question_ids = ["12345678-1234-5678-1234-567812345681",
                        "12345678-1234-5678-1234-567812345680"]

        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       question_ids=question_ids)

        attempt_storage = AttemptStorage()

        result = attempt_storage.get_assessment_attempted_questions(
            assessment_id=assessment_id, user_id=user_id)

        snapshot.assert_match(str(result),
                              "test_get_assessment_attempted_questions.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_get_assessment_attempt(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"
        question_ids = ["12345678-1234-5678-1234-567812345681",
                        "12345678-1234-5678-1234-567812345680"]
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51, 922886)

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       question_ids=question_ids, started_at=start_time)

        attempt_storage = AttemptStorage()

        result = attempt_storage.get_assessment_attempt(attempt_id=attempt_id)

        snapshot.assert_match(repr(result), "test_get_assessment_attempt.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_get_assessment_progress(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51, 922886)

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       started_at=start_time)

        attempt_storage = AttemptStorage()

        result = attempt_storage.get_assessment_progress(attempt_id=attempt_id)

        snapshot.assert_match(repr(result), "test_get_assessment_progress.txt")

    @pytest.mark.django_db
    def test_check_attempt_exist(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        attempt_id = "12345678-1234-5678-1234-567812345670"

        user = UserFactory(user_id=user_id)
        AttemptFactory(attempt_id=attempt_id, user=user)

        attempt_storage = AttemptStorage()

        result = attempt_storage.check_attempt_exist(attempt_id=attempt_id)

        snapshot.assert_match(repr(result), "test_check_attempt_exists.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_complete_assessment_attempt(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51, 922886)

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       started_at=start_time)

        attempt_storage = AttemptStorage()

        result = attempt_storage.complete_assessment_attempt(
            attempt_id=attempt_id)

        snapshot.assert_match(repr(result),
                              "test_complete_assessment_attempt.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_update_assessment_total_points(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51, 922886)

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       total_points=Decimal("10.0"), started_at=start_time)

        attempt_storage = AttemptStorage()

        result = attempt_storage.update_assessment_total_points(
            attempt_id=attempt_id, points=5.0)

        snapshot.assert_match(repr(result),
                              "test_update_assessment_total_points.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_end_an_attempt(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345678"
        assessment_id = "12345678-1234-5678-1234-567812345679"
        attempt_id = "12345678-1234-5678-1234-567812345670"
        start_time = datetime.datetime(2025, 11, 18, 13, 21, 51, 922886)

        user = UserFactory(user_id=user_id)
        assessment = AssessmentFactory(assessment_id=assessment_id)
        AttemptFactory(attempt_id=attempt_id, user=user, assessment=assessment,
                       started_at=start_time)

        attempt_storage = AttemptStorage()

        result = attempt_storage.end_an_attempt(attempt_id=attempt_id,
                                                status=StatusEnum.COMPLETE)

        snapshot.assert_match(repr(result), "test_end_an_attempt.txt")
