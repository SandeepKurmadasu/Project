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
    questions=models.ManyToManyField(Question,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class QuestionSelectionConfig(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    question_bank=models.ForeignKey(QuestionBank,on_delete=models.CASCADE)
    number_of_questions=models.IntegerField()
    algorithm=models.CharField(max_length=10) #DIFFICULTY BASED
