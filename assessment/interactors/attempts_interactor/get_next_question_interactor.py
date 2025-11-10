"""Create the get next question interactor """
from cyber_edu_verse.assessment.interactors.dtos import DisplayQuestionDTO, \
    AssessmentAttemptProgressDTO, QuestionDTO
from cyber_edu_verse.assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from cyber_edu_verse.assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface


class GetNextQuestionInteractor:
    """Get the next question interactor"""

    def __init__(self, assessment_storage: AssessmentStorageInterface,
                 attempt_storage: AttemptStorageInterface,
                 question_storage: QuestionStorageInterface,
                 response_question_storage: AttemptSubmittedQuestionStorageInterface):
        self.assessment_storage = assessment_storage
        self.attempt_storage = attempt_storage
        self.question_storage = question_storage
        self.response_question_storage = response_question_storage

    def get_next_question(self, attempt_id: str,
                          assessment_id: str) -> DisplayQuestionDTO | AssessmentAttemptProgressDTO:
        """Return next unanswered question or mark assessment complete."""

        next_question = self.get_next_question_data(
            assessment_id=assessment_id,
            attempt_id=attempt_id)
        if not next_question:
            return self.complete_assessment(attempt_id=attempt_id)

        return DisplayQuestionDTO(
            question_id=next_question.question_id,
            question_text=next_question.question_text,
            options=next_question.options
        )

    def complete_assessment(self,
                            attempt_id: str) -> AssessmentAttemptProgressDTO:
        """ Update the assessment status complete"""
        return self.attempt_storage.complete_assessment_attempt(
            attempt_id=attempt_id)

    def get_next_question_data(self, assessment_id: str,
                               attempt_id: str) -> QuestionDTO | None:
        """Get the next question data """

        assessment_data = self.assessment_storage.get_assessment(
            assessment_id=assessment_id)
        all_assessment_questions = assessment_data.questions
        answered_questions = self.response_question_storage.get_answered_submission_questions(
            attempt_id=attempt_id)

        for each_question in all_assessment_questions:
            is_answered_question = each_question.question_id in answered_questions
            if not is_answered_question:
                return each_question
        return None
