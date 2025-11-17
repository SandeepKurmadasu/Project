import uuid
from decimal import Decimal

from django.db import models


class QuestionType(models.TextChoices):
    MCQ_SINGLE = "MCQ_SINGLE"
    MCQ_MULTI = "MCQ_MULTI"
    TRUE_FALSE = "TRUE_FALSE"
    FILL_BLANK = "FILL_BLANK"
    MATCH_PAIRS = "MATCH_PAIRS"


class Difficulty(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Assessment(models.Model):
    class AssessmentType(models.TextChoices):
        QUIZ = "QUIZ", "Quiz"
        MODULE_EXAM = "MODULE_EXAM", "Module Exam"
        COURSE_EXAM = "COURSE_EXAM", "Course Exam"
        ASSIGNMENT = "ASSIGNMENT", "Assignment"

    assessment_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    title = models.CharField(max_length=255, db_index=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    assessment_type = models.CharField(max_length=11,
                                       choices=AssessmentType.choices)
    description = models.TextField()
    no_of_questions = models.PositiveIntegerField()
    pass_marks = models.PositiveIntegerField(default=0)
    marks = models.PositiveIntegerField(default=0)
    pass_percentage = models.PositiveIntegerField()
    easy_count = models.PositiveIntegerField(null=True, blank=True)
    medium_count = models.PositiveIntegerField(null=True, blank=True)
    hard_count = models.PositiveIntegerField(null=True, blank=True)
    attempts_limit = models.IntegerField(null=True, blank=True)
    estimated_duration_in_minutes = models.IntegerField()
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
        "course_management.User",
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    total_points = models.DecimalField(max_digits=6, decimal_places=2,
                                       default=Decimal("0.00"))
    status = models.CharField(
        max_length=15,
        default=AttemptStatusEnum.START,
        choices=AttemptStatusEnum.choices,
        db_index=True,
    )
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    question_ids = models.JSONField(default=list, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "assessment"]),
            models.Index(fields=["status"]),
            models.Index(fields=["started_at"]),
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


class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20,
                                     choices=QuestionType.choices)
    difficulty = models.CharField(max_length=10,
                                  choices=Difficulty.choices)
    options = models.JSONField(null=True, blank=True)
    correct_answer = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class QuestionBank(models.Model):
    bank_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    title = models.CharField(max_length=255, db_index=True)
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE,
                                      related_name="assessment_question_bank",
                                      db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title


class QuestionBankQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="bank_question", db_index=True)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE,
                                      related_name="assessment_bank",
                                      db_index=True)
    order = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("question_bank", "order")
        indexes = [
            models.Index(fields=["question_bank", "order"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.question_bank.title} - {self.order}"


