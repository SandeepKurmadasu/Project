import pytest
from freezegun import freeze_time

from assessment.interactors.dtos import UserQuestionSubmittedDTO, AnswerStatus
from assessment.storages.attempt_question_submission import \
    AttemptQuestionSubmissionStorage
from assessment.tests.factories.storage_factories import AttemptFactory, \
    AssessmentAttemptQuestionSubmissionFactory, QuestionFactory


class TestAttemptQuestionSubmission:

    @pytest.mark.django_db
    def test_get_answered_submission_questions(self, snapshot):
        attempt_id = "12345678-1234-5678-1234-567812345670"

        attempt = AttemptFactory(attempt_id=attempt_id)
        q1 = QuestionFactory(
            question_id="12345678-1234-5678-1234-567812345678")
        q2 = QuestionFactory(
            question_id="12345678-1234-5678-1234-567812345679")

        AssessmentAttemptQuestionSubmissionFactory(attempt=attempt,
                                                   question=q1)
        AssessmentAttemptQuestionSubmissionFactory(attempt=attempt,
                                                   question=q2)

        storage = AttemptQuestionSubmissionStorage()

        result = storage.get_answered_submission_questions(
            attempt_id=attempt_id)

        snapshot.assert_match(str(result),
                              "test_get_answered_submission_questions.txt")

    @pytest.mark.django_db
    @freeze_time("2025-11-18 13:21:51.922886")
    def test_create_attempted_question(self, snapshot):
        attempt_id = "12345678-1234-5678-1234-567812345670"
        question_id = "12345678-1234-5678-1234-567812345678"
        response = "optionA"
        is_response_correct = AnswerStatus.CORRECT

        AttemptFactory(attempt_id=attempt_id)
        QuestionFactory(question_id=question_id)

        storage = AttemptQuestionSubmissionStorage()

        submission_dto = UserQuestionSubmittedDTO(
            attempt_id=attempt_id,
            question_id=question_id,
            response=response,
            is_correct=is_response_correct
        )

        result = storage.create_attempted_question(
            assessment_submission_details=submission_dto)

        snapshot.assert_match(repr(result),
                              "test_create_attempted_question.txt")

    @pytest.mark.django_db
    def test_get_attempt_questions(self, snapshot):
        attempt_id1 = "12345678-1234-5678-1234-567812345670"
        attempt_id2 = "12345678-1234-5678-1234-567812345671"

        attempt1 = AttemptFactory(attempt_id=attempt_id1)
        attempt2 = AttemptFactory(attempt_id=attempt_id2)

        q1 = QuestionFactory(
            question_id="12345678-1234-5678-1234-567812345678")
        q2 = QuestionFactory(
            question_id="12345678-1234-5678-1234-567812345679")

        AssessmentAttemptQuestionSubmissionFactory(attempt=attempt1,
                                                   question=q1)
        AssessmentAttemptQuestionSubmissionFactory(attempt=attempt2,
                                                   question=q2)

        storage = AttemptQuestionSubmissionStorage()

        result = storage.get_attempt_questions(
            attempt_ids=[attempt_id1, attempt_id2])

        snapshot.assert_match(str(result),
                              "test_get_attempt_questions.txt")
