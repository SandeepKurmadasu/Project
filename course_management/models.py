from django.db import models
import uuid
from typing import Any

class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField()
    is_active = models.BooleanField(default=True)
    otp_count = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    course_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    average_rating = models.IntegerField(default=0)
    estimated_duration = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title


class Module(models.Model):
    module_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    module_title = models.CharField(max_length=255)
    description = models.TextField()
    estimated_duration = models.IntegerField(default=0)  # in minutes
    sequence_order = models.IntegerField(default=0)  # Order within course
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'modules'
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.module_title} - {self.course.title}"


class Topic(models.Model):
    TOPIC_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('ARTICLE', 'Article'),
        ('QUIZ', 'Quiz'),
        ('EXERCISE', 'Exercise'),
        ('EXAM', 'Exam'),
    ]

    topic_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic_type = models.CharField(max_length=20, choices=TOPIC_TYPE_CHOICES)
    content = models.TextField()
    estimated_duration = models.IntegerField(default=0)
    sequence_order = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topics'
        ordering = ['sequence_order']

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.module_id = None

    def __str__(self):
        return f"{self.title} - {self.module.module_title}"


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    course_percentage = models.IntegerField(default=0)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ['user', 'course']

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)


    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class UserLearningPath(models.Model):
    user_learning_path_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learning_paths')
    current_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_learners')
    overall_percentage = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_learning_paths'
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Learning Path"


class UserTopicCompletion(models.Model):
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('LOCKED', 'Locked'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_completions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_completions')
    user_learning_path = models.ForeignKey(UserLearningPath, on_delete=models.CASCADE, related_name='topic_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LOCKED')
    percentage = models.IntegerField(default=0)
    is_unlocked = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_topic_completions'
        unique_together = ['user', 'topic', 'user_learning_path']

    def __str__(self):
        return f"{self.user.username} - {self.topic.title} - {self.status}"


class QuestionBank(models.Model):
    question_bank_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='question_banks', null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question_banks'

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('SINGLE_CHOICE', 'Single Choice'),
        ('MULTIPLE_CHOICE', 'Multiple Choice'),
        ('TRUE_FALSE', 'True/False'),
        ('FILL_BLANK', 'Fill in the Blank'),
        ('MATCH_PAIRS', 'Match the Pairs'),
    ]

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    question_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    question_text = models.TextField()
    options = models.JSONField(default=dict)  # Stores question options
    correct_answer = models.JSONField(default=dict)  # Stores correct answer(s)
    marks = models.IntegerField(default=1)
    explanation = models.TextField(blank=True)
    sequence_order = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.question_type} - {self.question_text[:50]}"


class Assessment(models.Model):
    ASSESSMENT_TYPE_CHOICES = [
        ('PRACTICE_QUIZ', 'Practice Quiz'),
        ('MODULE_EXAM', 'Module Exam'),
        ('COURSE_EXAM', 'Course Exam'),
        ('ASSIGNMENT', 'Assignment'),
    ]

    SELECTION_LOGIC_CHOICES = [
        ('FIXED', 'Fixed Set'),
        ('RANDOM', 'Random Pool'),
        ('DIFFICULTY_MIX', 'Difficulty Mix'),
    ]

    SCORING_TYPE_CHOICES = [
        ('FIXED', 'Fixed Scoring'),
        ('WEIGHTED', 'Weighted Scoring'),
        ('PARTIAL_CREDIT', 'Partial Credit'),
        ('SCALED', 'Scaled Scoring'),
    ]

    assessment_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='assessments')
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField()  # in minutes
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    max_attempts = models.IntegerField(default=1)
    selection_logic = models.CharField(max_length=20, choices=SELECTION_LOGIC_CHOICES)
    scoring_type = models.CharField(max_length=20, choices=SCORING_TYPE_CHOICES)
    number_of_questions = models.IntegerField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assessments'

    def __str__(self):
        return f"{self.title} - {self.assessment_type}"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('SUBMITTED', 'Submitted'),
        ('AUTO_SUBMITTED', 'Auto Submitted'),
        ('ABANDONED', 'Abandoned'),
    ]

    attempt_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    attempt_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(default=0)  # in seconds
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attempts'
        unique_together = ['user', 'assessment', 'attempt_number']

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} - Attempt {self.attempt_number}"


class AttemptQuestion(models.Model):
    STATUS_CHOICES = [
        ('NOT_ATTEMPTED', 'Not Attempted'),
        ('SKIPPED', 'Skipped'),
        ('ANSWERED', 'Answered'),
    ]

    id = models.AutoField(primary_key=True)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='attempt_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempt_questions')
    user_answer = models.JSONField(default=dict)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_ATTEMPTED')
    time_spent = models.IntegerField(default=0)
    sequence_number = models.IntegerField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attempt_questions'
        ordering = ['sequence_number']

    def __str__(self):
        return f"Attempt {self.attempt.attempt_id} - Q{self.sequence_number}"