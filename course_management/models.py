from django.db import models
import uuid

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
    prerequisites = models.TextField(null=True, blank=True)
    learning_objectives = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title


class Module(models.Model):
    module_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    module_title = models.CharField(max_length=255)
    description = models.TextField()
    estimated_duration_in_mins = models.IntegerField(default=0)
    sequence_order = models.IntegerField(default=0)
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
    # question_bank = models.OneToOneField(
    #     'assessment.QuestionBank',
    #     on_delete=models.CASCADE,
    #     related_name='topic',
    #     null=True,
    #     blank=True
    # )

    class Meta:
        db_table = 'topics'
        ordering = ['sequence_order']

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

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

TOPIC_PROGRESS_STATUS_CHOICES = [
    ('NOT_STARTED', 'Not Started'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
]

class UserTopicProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="topic_progresses")
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, related_name="user_progresses")

    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=TOPIC_PROGRESS_STATUS_CHOICES, default='NOT_STARTED')
    last_updated = models.DateTimeField(auto_now=True)


class CourseRating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')

    rating = models.IntegerField()
    feedback_comment = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)