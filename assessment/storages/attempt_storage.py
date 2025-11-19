from decimal import Decimal
from django.utils import timezone


from assessment.interactors.dtos import AssessmentAttemptDTO, \
    AssessmentAttemptProgressDTO
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.models import Attempt, Assessment
from course_management.interactors.dtos import StatusEnum
from course_management.models import User


class AttemptStorage(AttemptStorageInterface):

    def create_assessment_attempt(self, user_id: str,
                                  question_ids: list[str],
                                  assessment_id: str) -> AssessmentAttemptDTO:
        user = User.objects.get(user_id=user_id)
        assessment = Assessment.objects.get(assessment_id=assessment_id)

        created_data = Attempt.objects.create(user=user, assessment=assessment,
                                              question_ids=question_ids)

        return AssessmentAttemptDTO(
            attempt_id=created_data.attempt_id,
            assessment_id=created_data.assessment.assessment_id,
            user_id=user_id,
            question_ids=created_data.question_ids,
            total_points=created_data.total_points,
            status=created_data.status,
            started_at=created_data.started_at
        )

    def get_latest_assessment_attempt(self, user_id: str,
                                      assessment_id: str) -> AssessmentAttemptDTO:
        attempt = Attempt.objects.filter(user_id=user_id,
                                         assessment_id=assessment_id).last()
        return AssessmentAttemptDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=assessment_id,
            user_id=user_id,
            total_points=attempt.total_points,
            question_ids=attempt.question_ids,
            status=attempt.status,
            started_at=attempt.started_at
        )

    def get_assessment_attempted_questions(self, assessment_id: str,
                                           user_id: str) -> list[str]:

        return list(Attempt.objects.filter(user_id=user_id,
                                           assessment_id=assessment_id).values_list(
            'attempt_id', flat=True))

    def get_assessment_attempt(self, attempt_id: str) -> AssessmentAttemptDTO:
        attempt = Attempt.objects.get(attempt_id=attempt_id)

        return AssessmentAttemptDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment.assessment_id,
            user_id=attempt.user.user_id,
            total_points=attempt.total_points,
            question_ids=attempt.question_ids,
            status=attempt.status,
            started_at=attempt.started_at
        )

    def get_assessment_progress(self,
                                attempt_id: str) -> AssessmentAttemptProgressDTO:
        attempt = Attempt.objects.get(attempt_id=attempt_id)

        return AssessmentAttemptProgressDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment.assessment_id,
            user_id=attempt.user.user_id,
            total_points=attempt.total_points,
            status=attempt.status,
        )

    def check_attempt_exist(self, attempt_id: str) -> bool:

        return Attempt.objects.filter(attempt_id=attempt_id).exists()

    def complete_assessment_attempt(self,
                                    attempt_id: str) -> AssessmentAttemptProgressDTO:
        attempt = Attempt.objects.get(attempt_id=attempt_id)
        attempt.status = StatusEnum.COMPLETE
        attempt.completed_at = timezone.now()
        attempt.save()

        return AssessmentAttemptProgressDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment.assessment_id,
            user_id=attempt.user.user_id,
            total_points=attempt.total_points,
            status=attempt.status,
        )

    def update_assessment_total_points(self, attempt_id: str,
                                       points: float) -> AssessmentAttemptDTO:
        attempt = Attempt.objects.get(attempt_id=attempt_id)
        attempt.total_points += Decimal(str(points))
        attempt.save()

        return AssessmentAttemptDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment.assessment_id,
            user_id=attempt.user.user_id,
            total_points=attempt.total_points,
            question_ids=attempt.question_ids,
            status=attempt.status,
            started_at=attempt.started_at
        )

    def end_an_attempt(self, attempt_id: str,
                       status: StatusEnum.COMPLETE) -> AssessmentAttemptDTO:
        attempt = Attempt.objects.get(attempt_id=attempt_id)
        attempt.status = StatusEnum.COMPLETE
        attempt.completed_at = timezone.now()
        attempt.save()

        return AssessmentAttemptDTO(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment.assessment_id,
            user_id=attempt.user.user_id,
            total_points=attempt.total_points,
            question_ids=attempt.question_ids,
            status=attempt.status,
            started_at=attempt.started_at
        )
