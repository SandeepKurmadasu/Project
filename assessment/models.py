import uuid
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


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    topic = models.ForeignKey("course_management.Topic", on_delete=models.CASCADE)
    options = models.JSONField(null=True, blank=True)
    correct_option_ids = models.JSONField(null=True, blank=True)   # MCQ_SINGLE/MULTI
    correct_boolean = models.BooleanField(null=True, blank=True)   # TRUE_FALSE
    correct_fill_text = models.CharField(max_length=255, null=True, blank=True)  # FILL_IN_THE_BLANK
    correct_pairs = models.JSONField(null=True, blank=True)        # MATCH_THE_PAIRS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class QuestionBank(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    name=models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE,related_name="assessment_question_bank",db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
