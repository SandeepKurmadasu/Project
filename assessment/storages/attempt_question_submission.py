from assessment.interactors.dtos import \
    UserQuestionSubmittedDTO, QuestionDTO
from assessment.interactors.storage_interface.attempt_submitted_questions_storage_interface import \
    AttemptSubmittedQuestionStorageInterface
from assessment.models import \
    AssessmentAttemptQuestionSubmission, Attempt, Question


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
        return UserQuestionSubmittedDTO(
            attempt_id=obj.attempt.attempt_id,
            question_id=obj.question.question_id,
            response=obj.selected_option,
            is_correct=obj.is_response_correct
        )

    def get_attempt_questions(self, attempt_ids: list[str]) -> list[str]:
        attempted_questions = AssessmentAttemptQuestionSubmission.objects.filter(
            attempt_id__in=attempt_ids)

        return [obj.question.question_id for obj in attempted_questions]
