# pylint: disable=too-few-public-methods
""" Create the submit question response interactor"""
from cyber_edu_verse.assessment.interactors.assessment_validations import \
    AssessmentValidationMixIn
from cyber_edu_verse.assessment.interactors.dtos import SubmitResponseDTO, \
    UserQuestionSubmittedDTO, ScoreResponseDTO
from cyber_edu_verse.assessment.interactors.question.evaluate_question import \
    EvaluateQuestionInteractor
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.question_storage_interface import \
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
            answer=submit_details.response)

        question = self.question_storage.get_questions(question_ids=[submit_details.question_id])[0]

        user_response_input = UserQuestionSubmittedDTO(
            attempt_id=submit_details.attempt_id,
            question_id=submit_details.question_id,
            response=submit_details.response,
            is_correct=answer
        )
        self.question_response_storage.create_attempted_question(
            assessment_submission_details=user_response_input)

        get_score_input = ScoreResponseDTO(
            question_response=answer.CORRECT,
            question_difficulty=question.difficulty_level,
            correct_options_count= 0,
            total_option_count= 1
        )

        score = self.get_question_scoring(user_response_data=get_score_input)

        if answer:
            result = self.attempt_storage.update_assessment_total_points(
                attempt_id=submit_details.attempt_id,
                points=score)
        else:
            result = self.attempt_storage.update_assessment_total_points(
                attempt_id=submit_details.attempt_id,
                points=score)

        return result
