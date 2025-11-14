# pylint: disable=too-few-public-methods
""" Create the submit question response interactor"""
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import SubmitResponseDTO, \
    UserQuestionSubmittedDTO, ScoreResponseDTO, AnswerStatus, ScoreConfigDTO, \
    ResponseEnum
from assessment.interactors.evaluate_questions.evaluate_question_interactor import \
    EvaluateQuestionInteractor

from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface


class SubmitQuestionInteractor(AssessmentValidationMixIn):
    """submit the question response interactor"""

    def __init__(self, question_storage: QuestionStorageInterface,
                 attempt_storage: AttemptStorageInterface,
                 question_response_storage: AttemptSubmittedQuestionStorageInterface):
        self.question_storage = question_storage
        self.attempt_storage = attempt_storage
        self.question_response_storage = question_response_storage

    def submit_question_response(self, submit_details: SubmitResponseDTO):
        """evaluate and update the attempt data """
        evaluate_interactor = EvaluateQuestionInteractor(
            storage=self.question_storage)
        answer = evaluate_interactor.evaluate(
            question_id=submit_details.question_id,
            user_answer=submit_details.response)

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
            question_response=answer.is_correct.CORRECT,
            question_difficulty=question.difficulty_level,
            correct_options_count=answer.correct_count,
            total_option_count=answer.total_count
        )

        score = self.get_question_scoring(user_response_data=get_score_input)

        result = self.attempt_storage.update_assessment_total_points(
            attempt_id=submit_details.attempt_id,
            points=score)

        return result

    @staticmethod
    def get_question_scoring(user_response_data: ScoreResponseDTO) -> float:
        scoring_config = ScoreConfigDTO.points.get(
            user_response_data.question_difficulty)

        if user_response_data.question_response == ResponseEnum.WRONG:
            base_score = scoring_config[ResponseEnum.WRONG]
        elif user_response_data.question_response == ResponseEnum.CORRECT:
            base_score = scoring_config[ResponseEnum.CORRECT]
        else:
            user_getting_percentage = (
                    user_response_data.correct_options_count / user_response_data.total_option_count)
            base_score = user_getting_percentage * scoring_config[
                ResponseEnum.CORRECT]

        return base_score
