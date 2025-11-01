import uuid
from enum import Enum
from typing import Any

from django.db import models

import course_management.models

LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
DIFFICULTY= [
    ('EASY', 'Easy'),
    ('MEDIUM', 'Medium'),
    ('HARD', 'Hard'),
]

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Question(models.Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.correct_option_ids = None
        self.options = None

    question_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    question_text=models.CharField(max_length=100)
    question_type=models.CharField(max_length=20, choices= LEVEL_CHOICES)
    difficulty=models.CharField(max_length=20, choices=DIFFICULTY)
    topics=models.ForeignKey(course_management.models.Topic,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)