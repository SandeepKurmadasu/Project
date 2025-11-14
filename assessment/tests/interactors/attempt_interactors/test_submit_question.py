import datetime
from unittest.mock import create_autospec, MagicMock
from freezegun import freeze_time

from assessment.interactors.attempts_interactor.submit_question import \
    SubmitQuestionInteractor
from assessment.interactors.dtos import SubmitResponseDTO, \
    AssessmentAttemptDTO, Difficulty, AnswerStatus

from assessment.interactors.storage_interface.assessment_attempt_storage_interface import (
    AttemptStorageInterface,
)
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import (
    AttemptSubmittedQuestionStorageInterface,
)
from assessment.interactors.storage_interface.question_storage_interface import (
    QuestionStorageInterface,
)
from course_management.interactors.dtos import StatusEnum


class TestSubmitQuestionInteractor:

    def setup_method(self):
        self.attempt_storage = create_autospec(AttemptStorageInterface)
        self.question_storage = create_autospec(QuestionStorageInterface)
        self.question_response_storage = create_autospec(
            AttemptSubmittedQuestionStorageInterface
        )

        self.interactor = SubmitQuestionInteractor(
            question_storage=self.question_storage,
            attempt_storage=self.attempt_storage,
            question_response_storage=self.question_response_storage,
        )

        # Mock attempt responses for different cases
        self.updated_attempt_correct = AssessmentAttemptDTO(
            attempt_id="attempt-101",
            user_id="user-1",
            assessment_id="assessment-1234",
            total_points=5,
            question_ids=[],
            status=StatusEnum.COMPLETE,
            started_at=datetime.datetime(2024, 10, 31, 10, 0, 0),
        )

        self.updated_attempt_wrong = AssessmentAttemptDTO(
            attempt_id="attempt-101",
            user_id="user-1",
            assessment_id="assessment-1234",
            total_points=0,
            question_ids=[],
            status=StatusEnum.IN_PROGRESS,
            started_at=datetime.datetime(2024, 10, 31, 10, 0, 0),
        )

        self.updated_attempt_partial = AssessmentAttemptDTO(
            attempt_id="attempt-101",
            user_id="user-1",
            assessment_id="assessment-1234",
            total_points=3,
            question_ids=[],
            status=StatusEnum.IN_PROGRESS,
            started_at=datetime.datetime(2024, 10, 31, 10, 0, 0),
        )

        # Mock question
        self.mock_question = MagicMock()
        self.mock_question.difficulty_level = Difficulty.MEDIUM

    @staticmethod
    def _make_mock_answer(is_correct, correct_count=1):
        """Helper to mock EvaluateQuestionInteractor return value"""
        mock_answer = MagicMock()
        mock_answer.is_correct = is_correct
        mock_answer.correct_count = correct_count
        return mock_answer

    @freeze_time("2024-10-31 10:00:00")
    def test_submit_question_correct_answer(self, snapshot, monkeypatch):
        submit_details = SubmitResponseDTO(
            assessment_id="assessment-1234",
            attempt_id="attempt-101",
            question_id="Q1",
            response="correct-opt",
        )

        mock_answer = self._make_mock_answer(AnswerStatus.CORRECT,
                                             correct_count=2)
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.EvaluateQuestionInteractor.evaluate",
            MagicMock(return_value=mock_answer),
        )
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.SubmitQuestionInteractor.get_question_scoring",
            lambda *args, **kwargs: 5,
        )

        self.question_storage.get_questions.return_value = [self.mock_question]
        self.attempt_storage.update_assessment_total_points.return_value = (
            self.updated_attempt_correct
        )

        result = self.interactor.submit_question_response(submit_details)

        self.attempt_storage.update_assessment_total_points.assert_called_once_with(
            attempt_id="attempt-101", points=5
        )
        snapshot.assert_match(repr(result),
                              "submit_correct_answer_snapshot.json")

    @freeze_time("2024-10-31 10:00:00")
    def test_submit_question_wrong_answer(self, snapshot, monkeypatch):
        submit_details = SubmitResponseDTO(
            assessment_id="assessment-1234",
            attempt_id="attempt-101",
            question_id="Q1",
            response="wrong-opt",
        )

        mock_answer = self._make_mock_answer(AnswerStatus.INCORRECT,
                                             correct_count=0)
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.EvaluateQuestionInteractor.evaluate",
            MagicMock(return_value=mock_answer),
        )
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.SubmitQuestionInteractor.get_question_scoring",
            lambda *args, **kwargs: 0,
        )

        self.question_storage.get_questions.return_value = [self.mock_question]
        self.attempt_storage.update_assessment_total_points.return_value = (
            self.updated_attempt_wrong
        )

        result = self.interactor.submit_question_response(submit_details)

        self.attempt_storage.update_assessment_total_points.assert_called_once_with(
            attempt_id="attempt-101", points=0
        )
        snapshot.assert_match(repr(result),
                              "submit_wrong_answer_snapshot.json")

    @freeze_time("2024-10-31 10:00:00")
    def test_submit_question_partial_answer(self, snapshot, monkeypatch):
        submit_details = SubmitResponseDTO(
            assessment_id="assessment-1234",
            attempt_id="attempt-101",
            question_id="Q1",
            response="partial-opt",
        )

        mock_answer = self._make_mock_answer(AnswerStatus.PARTIALLY_CORRECT,
                                             correct_count=1)
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.EvaluateQuestionInteractor.evaluate",
            MagicMock(return_value=mock_answer),
        )
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.SubmitQuestionInteractor.get_question_scoring",
            lambda *args, **kwargs: 3,
        )

        self.question_storage.get_questions.return_value = [self.mock_question]
        self.attempt_storage.update_assessment_total_points.return_value = (
            self.updated_attempt_partial
        )

        result = self.interactor.submit_question_response(submit_details)

        self.attempt_storage.update_assessment_total_points.assert_called_once_with(
            attempt_id="attempt-101", points=3
        )
        snapshot.assert_match(repr(result),
                              "submit_partial_answer_snapshot.json")

    @freeze_time("2024-10-31 10:00:00")
    def test_submit_question_partial_answer_zero_correct_options(self,
                                                                 snapshot,
                                                                 monkeypatch):
        submit_details = SubmitResponseDTO(
            assessment_id="assessment-1234",
            attempt_id="attempt-101",
            question_id="Q1",
            response="partial-opt",
        )

        mock_answer = self._make_mock_answer(AnswerStatus.PARTIALLY_CORRECT,
                                             correct_count=0)
        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.EvaluateQuestionInteractor.evaluate",
            MagicMock(return_value=mock_answer),
        )

        def scoring_mock(*args, **kwargs):
            dto = kwargs.get("user_response_data")
            if dto.correct_options_count == 0:
                return 0
            return 2

        monkeypatch.setattr(
            "assessment.interactors.attempts_interactor.submit_question.SubmitQuestionInteractor.get_question_scoring",
            scoring_mock,
        )

        self.question_storage.get_questions.return_value = [self.mock_question]
        self.attempt_storage.update_assessment_total_points.return_value = (
            self.updated_attempt_wrong
        )

        result = self.interactor.submit_question_response(submit_details)

        self.attempt_storage.update_assessment_total_points.assert_called_once_with(
            attempt_id="attempt-101", points=0
        )
        snapshot.assert_match(repr(result),
                              "submit_partial_zero_correct_options_snapshot.json")
