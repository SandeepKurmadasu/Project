import uuid
from django.db import models


class Assessment(models.Model):
    class AssessmentType(models.TextChoices):
        QUIZ = "QUIZ", "Quiz"
        MODULE_EXAM = "MODULE_EXAM", "Module Exam"
        COURSE_EXAM = "COURSE_EXAM", "Course Exam"
        ASSIGNMENT = "ASSIGNMENT", "Assignment"


    assessment_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    title = models.CharField(max_length=255, db_index=True)
    icon = models.CharField(max_length=255,null=True,blank=True)
    assessment_type = models.CharField(max_length=11,choices=AssessmentType.choices)
    description = models.TextField()
    pass_marks = models.IntegerField()
    estimated_duration_in_minutes = models.IntegerField()
    marks = models.IntegerField()
    attempts_limit = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title


class Attempt(models.Model):
    class AttemptStatusEnum(models.TextChoices):
        START = "START", "Start"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETE = "COMPLETE", "Complete"

    attempt_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    total_points = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    status = models.CharField(
        max_length=15,
        default=AttemptStatusEnum.START,
        choices=AttemptStatusEnum.choices,
        db_index=True,
    )
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "assessment"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}"


class AssessmentAttemptQuestionSubmission(models.Model):
    class Response(models.TextChoices):
        CORRECT = "CORRECT", "Correct"
        WRONG = "WRONG", "Wrong"
        PARTIAL_CORRECT = "PARTIAL_CORRECT", "Partial Correct"

    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name="question_submissions",
    )
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="attempt_submissions",
    )
    selected_option = models.CharField(max_length=255)
    is_response_correct = models.CharField(max_length=15,
                                           default=Response.WRONG,
                                           choices=Response.choices,
                                           db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["attempt"]),
            models.Index(fields=["question"]),
            models.Index(fields=["is_response_correct"]),
        ]

    def __str__(self):
        return f"Attempt {self.attempt.attempt_id} - {self.question}"
