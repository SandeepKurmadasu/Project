from assessment.interactors.dtos import \
    UserQuestionSubmittedDTO
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.models import \
    AssessmentAttemptQuestionSubmission, Attempt


class AttemptQuestionSubmissionStorage(
    AttemptSubmittedQuestionStorageInterface):

    def get_answered_submission_questions(self, attempt_id: str) -> list[str]:
        attempts = AssessmentAttemptQuestionSubmission.objects.filter(
            attempt_id=attempt_id)

        return [attempt.question.question_id for attempt in attempts]

    def create_attempted_question(self,
                                  assessment_submission_details: UserQuestionSubmittedDTO) \
            -> UserQuestionSubmittedDTO:
        attempt = Attempt.objects.get(
            attempt_id=assessment_submission_details.attempt_id)
        question = Question.objects.get(
            question_id=assessment_submission_details.question_id)

        obj = AssessmentAttemptQuestionSubmission.objects.create(
            attempt=attempt, question=question,
            selected_option=assessment_submission_details.response,
            is_response_correct=assessment_submission_details.is_correct)
        return obj
