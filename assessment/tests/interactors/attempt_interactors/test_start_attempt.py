import datetime

import pytest
from unittest.mock import create_autospec, MagicMock

from assessment.exceptions.custom_exceptions import AssessmentIdNotFound
from assessment.interactors.attempts_interactor.start_assessment_attempt_interactor import \
    StartAssessmentAttemptInteractor
from assessment.interactors.dtos import AssessmentTypeEnum, Difficulty, \
    AssessmentAttemptDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_question_storage_interface import \
    QuestionBankQuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import \
    QuestionBankStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface

from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.interactors.dtos import StatusEnum
from course_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)


class MockQuestionDTO:
    def __init__(self, question_id, difficulty_level, question_text="", options=None, marks=10):
        self.question_id = question_id
        self.difficulty_level = difficulty_level
        self.question_text = question_text
        self.options = options or []
        self.marks = marks


class TestStartAssessmentAttemptInteractor:
    start_time = datetime.datetime(2025, 11, 11, 12, 30, 00)

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.assessments_storage = create_autospec(AssessmentStorageInterface)
        self.question_storage = create_autospec(QuestionStorageInterface)
        self.question_bank_storage = create_autospec(
            QuestionBankStorageInterface)
        self.user_submitted_question_storage = create_autospec(
            AttemptSubmittedQuestionStorageInterface)
        self.question_bank_question_storage = create_autospec(
            QuestionBankQuestionStorageInterface)

        self.interactor = StartAssessmentAttemptInteractor(
            attempt_storage=self.attempt_storage,
            user_storage=self.user_storage,
            assessments_storage=self.assessments_storage,
            question_storage=self.question_storage,
            question_bank_storage=self.question_bank_storage,
            user_question_submitted_storage=self.user_submitted_question_storage,
            question_bank_question_storage=self.question_bank_question_storage
        )

    def test_start_assessment_attempt_quiz_success(self, snapshot):
        user_id = "user-001"
        assessment_id = "assess-123"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.return_value = True

        mock_assessment = MagicMock()
        mock_assessment.assessment_type = AssessmentTypeEnum.QUIZ
        mock_assessment.no_of_questions = 3
        mock_assessment.pass_percentage = 50
        mock_assessment.easy_count = 1
        mock_assessment.medium_count = 1
        mock_assessment.hard_count = 1
        mock_assessment.marks = 30
        mock_assessment.pass_marks = 15
        mock_assessment.assessment_id = assessment_id
        mock_assessment.attempts_limit = 0   # ← ADDED
        self.assessments_storage.get_assessment.return_value = mock_assessment

        mock_bank_data = MagicMock()
        mock_bank_data.bank_id = "bank-001"
        self.question_bank_storage.get_assessment_question_bank.return_value = mock_bank_data

        mock_questions = [
            MockQuestionDTO("q1", Difficulty.EASY),
            MockQuestionDTO("q2", Difficulty.MEDIUM),
            MockQuestionDTO("q3", Difficulty.HARD),
        ]
        self.interactor.get_next_n_questions = MagicMock(return_value=mock_questions)

        expected_attempt = AssessmentAttemptDTO(
            attempt_id="attempt-123",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=0,
            question_ids=["q1", "q2", "q3"],
            status=StatusEnum.START,
            started_at=self.start_time
        )
        self.attempt_storage.create_assessment_attempt.return_value = expected_attempt

        result = self.interactor.start_assessment_attempt(user_id, assessment_id)
        snapshot.assert_match(repr(result), "quiz_success.json")

    def test_start_assessment_attempt_module_exam_success(self, snapshot):
        user_id = "user-010"
        assessment_id = "assess-200"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.return_value = True

        mock_assessment = MagicMock()
        mock_assessment.assessment_type = AssessmentTypeEnum.MODULE_EXAM
        mock_assessment.no_of_questions = 2
        mock_assessment.pass_percentage = 40
        mock_assessment.easy_count = 1
        mock_assessment.medium_count = 0
        mock_assessment.hard_count = 1
        mock_assessment.marks = 20
        mock_assessment.pass_marks = 8
        mock_assessment.assessment_id = assessment_id
        mock_assessment.attempts_limit = 0   # ← ADDED
        self.assessments_storage.get_assessment.return_value = mock_assessment

        mock_bank = MagicMock()
        mock_bank.bank_id = "bank-xyz"
        self.question_bank_storage.get_assessment_question_bank.return_value = mock_bank

        mock_questions = [
            MockQuestionDTO("q11", Difficulty.EASY),
            MockQuestionDTO("q22", Difficulty.HARD),
        ]
        self.interactor.get_next_n_questions = MagicMock(return_value=mock_questions)

        expected_attempt = AssessmentAttemptDTO(
            attempt_id="attempt-200",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=0,
            question_ids=["q11", "q22"],
            status=StatusEnum.START,
            started_at=self.start_time
        )
        self.attempt_storage.create_assessment_attempt.return_value = expected_attempt

        result = self.interactor.start_assessment_attempt(user_id, assessment_id)
        snapshot.assert_match(repr(result), "module_exam_success.json")

    def test_start_assessment_attempt_course_exam_success(self, snapshot):
        user_id = "usr-301"
        assessment_id = "exam-301"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.return_value = True

        mock_assessment = MagicMock()
        mock_assessment.assessment_type = AssessmentTypeEnum.COURSE_EXAM
        mock_assessment.no_of_questions = 3
        mock_assessment.pass_percentage = 70
        mock_assessment.easy_count = 1
        mock_assessment.medium_count = 1
        mock_assessment.hard_count = 1
        mock_assessment.marks = 30
        mock_assessment.pass_marks = 21
        mock_assessment.assessment_id = assessment_id
        mock_assessment.attempts_limit = 0   # ← ADDED
        self.assessments_storage.get_assessment.return_value = mock_assessment

        mock_bank = MagicMock()
        mock_bank.bank_id = "bank-301"
        self.question_bank_storage.get_assessment_question_bank.return_value = mock_bank

        mock_questions = [
            MockQuestionDTO("qe1", Difficulty.EASY),
            MockQuestionDTO("qe2", Difficulty.MEDIUM),
            MockQuestionDTO("qe3", Difficulty.HARD),
        ]
        self.interactor.get_next_n_questions = MagicMock(return_value=mock_questions)

        expected_attempt = AssessmentAttemptDTO(
            attempt_id="att-301",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=0,
            question_ids=["qe1", "qe2", "qe3"],
            status=StatusEnum.START,
            started_at=self.start_time
        )
        self.attempt_storage.create_assessment_attempt.return_value = expected_attempt

        result = self.interactor.start_assessment_attempt(user_id, assessment_id)
        snapshot.assert_match(repr(result), "course_exam_success.json")

    def test_start_assessment_attempt_skips_previous_questions(self, snapshot):
        user_id = "usr-prev"
        assessment_id = "ass-prev"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.return_value = True

        mock_assessment = MagicMock()
        mock_assessment.assessment_type = AssessmentTypeEnum.MODULE_EXAM
        mock_assessment.no_of_questions = 2
        mock_assessment.pass_percentage = 50
        mock_assessment.easy_count = 1
        mock_assessment.medium_count = 1
        mock_assessment.hard_count = 0
        mock_assessment.marks = 20
        mock_assessment.pass_marks = 10
        mock_assessment.assessment_id = assessment_id
        mock_assessment.attempts_limit = 0   # ← ADDED
        self.assessments_storage.get_assessment.return_value = mock_assessment

        mock_bank = MagicMock()
        mock_bank.bank_id = "bank-prev"
        self.question_bank_storage.get_assessment_question_bank.return_value = mock_bank

        self.attempt_storage.get_assessment_attempted_questions.return_value = [
            MagicMock(question_id="q-old")
        ]

        new_questions = [
            MockQuestionDTO("q-new1", Difficulty.EASY),
            MockQuestionDTO("q-new2", Difficulty.MEDIUM),
        ]
        self.interactor.get_next_n_questions = MagicMock(return_value=new_questions)

        expected_attempt = AssessmentAttemptDTO(
            attempt_id="att-prev",
            user_id=user_id,
            assessment_id=assessment_id,
            total_points=0,
            question_ids=["q-new1", "q-new2"],
            status=StatusEnum.START,
            started_at=self.start_time
        )
        self.attempt_storage.create_assessment_attempt.return_value = expected_attempt

        result = self.interactor.start_assessment_attempt(user_id, assessment_id)
        snapshot.assert_match(repr(result), "skip_old_questions.json")


    def test_start_assessment_attempt_user_not_found(self):
        user_id = "invalid-user"
        assessment_id = "assess-123"

        self.user_storage.check_user_exists.side_effect = UserNotFound(user_id)

        with pytest.raises(UserNotFound):
            self.interactor.start_assessment_attempt(user_id, assessment_id)

        self.assessments_storage.get_assessment.assert_not_called()
        self.attempt_storage.create_assessment_attempt.assert_not_called()

    def test_start_assessment_attempt_assessment_not_found(self):
        user_id = "user-001"
        assessment_id = "assessment-1234"

        self.user_storage.check_user_exists.return_value = True
        self.assessments_storage.assessment_exists.side_effect = AssessmentIdNotFound(
            assessment_id)

        with pytest.raises(AssessmentIdNotFound):
            self.interactor.start_assessment_attempt(user_id, assessment_id)

        self.attempt_storage.create_assessment_attempt.assert_not_called()
