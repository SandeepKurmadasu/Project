# pylint: disable=too-few-public-methods
""" Create the submit question response interactor"""
from uuid import UUID

from assessment.exceptions.custom_exceptions import AlreadyAttemptedExist
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import SubmitResponseDTO, \
    UserQuestionSubmittedDTO, ScoreResponseDTO, ScoreConfigDTO, ResponseEnum, \
    AnswerStatus, AssessmentTypeEnum
from assessment.interactors.evaluate_questions.evaluate_question_interactor import \
    EvaluateQuestionInteractor

from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface


class SubmitQuestionInteractor(AssessmentValidationMixIn):
    """submit the question response interactor"""

    def __init__(self, question_storage: QuestionStorageInterface,
                 attempt_storage: AttemptStorageInterface,
                 question_response_storage: AttemptSubmittedQuestionStorageInterface,
                 assessment_storage: AssessmentStorageInterface):
        self.question_storage = question_storage
        self.attempt_storage = attempt_storage
        self.question_response_storage = question_response_storage
        self.assessment_storage = assessment_storage

    def submit_question_response(self, submit_details: SubmitResponseDTO):
        """evaluate and update the attempt data """

        assessment_data = self.assessment_storage.get_assessment(assessment_id=submit_details.assessment_id)
        evaluate_interactor = EvaluateQuestionInteractor(
            storage=self.question_storage)
        answer = evaluate_interactor.evaluate(
            question_id=submit_details.question_id,
            user_answer=submit_details.response)

        self.check_question_already_attempted(
            question_id=submit_details.question_id,
            attempt_id=submit_details.attempt_id)


        question = self.question_storage.get_questions(
            question_ids=[submit_details.question_id])[0]

        user_response_input = UserQuestionSubmittedDTO(
            attempt_id=submit_details.attempt_id,
            question_id=submit_details.question_id,
            response=submit_details.response,
            is_correct=answer.is_correct
        )
        self.question_response_storage.create_attempted_question(
            assessment_submission_details=user_response_input)


        get_score_input = ScoreResponseDTO(
            question_response=answer.is_correct,
            question_difficulty=question.difficulty_level,
            correct_options_count=answer.correct_count,
            total_option_count=answer.total_count,
            assessment_type=assessment_data.assessment_type
        )

        score = self.get_question_scoring(user_response_data=get_score_input)

        result = self.attempt_storage.update_assessment_total_points(
            attempt_id=submit_details.attempt_id,
            points=score)

        return result


    def get_question_scoring(self,user_response_data: ScoreResponseDTO) -> float:
        if user_response_data.assessment_type == AssessmentTypeEnum.QUIZ.value:

            if user_response_data.question_response == AnswerStatus.CORRECT:
                return self.fixed_scoring(True)

            elif user_response_data.question_response == AnswerStatus.INCORRECT:
                return self.fixed_scoring(False)

            percentage = (
                    user_response_data.correct_options_count / user_response_data.total_option_count
            )
            return percentage * self.fixed_scoring(True)

        scoring_config = ScoreConfigDTO.points.get(
            user_response_data.question_difficulty
        )

        if user_response_data.question_response == AnswerStatus.INCORRECT:
            return scoring_config[ResponseEnum.WRONG]

        if user_response_data.question_response == AnswerStatus.CORRECT:
            return scoring_config[ResponseEnum.CORRECT]

        percentage = (
                user_response_data.correct_options_count / user_response_data.total_option_count
        )
        return percentage * scoring_config[ResponseEnum.CORRECT]

    def check_question_already_attempted(self, question_id: str,
                                         attempt_id: str):
        attempted_questions = self.question_response_storage.get_answered_submission_questions(
            attempt_id=attempt_id)

        if UUID(question_id) in attempted_questions:
            raise AlreadyAttemptedExist(question_id=question_id)
