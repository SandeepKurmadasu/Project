import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Course(models.Model):
    class CourseCategoryEnum(models.TextChoices):
        DEVELOPMENT = "DEVELOPMENT", "Development"
        DESIGN = "DESIGN", "Design"
        MARKETING = "MARKETING", "Marketing"
        BUSINESS = "BUSINESS", "Business"

    class LevelEnum(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20,
                                choices=CourseCategoryEnum.choices,
                                db_index=True)
    level = models.CharField(max_length=15, choices=LevelEnum.choices,
                             db_index=True)
    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    estimated_duration_in_min = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return self.title


class Module(models.Model):
    module_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    course = models.ForeignKey(Course, related_name="modules",
                               on_delete=models.CASCADE,
                               db_index=True, null=True, blank=True)
    module_title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, db_index=True)
    estimated_duration_in_min = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["module_title", "created_at"]),
        ]

    def __str__(self):
        return self.module_title


class Topic(models.Model):
    class TopicTypeEnum(models.TextChoices):
        LEARNING = "LEARNING", "Learning"
        ASSESSMENT = "ASSESSMENT", "Assessment"

    topic_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                               related_name="module_topic", db_index=True)
    topic_title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    topic_type = models.CharField(max_length=15, choices=TopicTypeEnum.choices,
                                  db_index=True)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0, db_index=True)
    estimated_duration_in_mins = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["module", "order"]),
        ]

    def __str__(self):
        return self.topic_title


class User(models.Model):
    class GenderEnum(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHERS = "OTHERS", "Others"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    gender = models.CharField(max_length=7, choices=GenderEnum.choices)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    otp_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return self.username


class Enrollment(models.Model):
    class EnrollmentStatusEnum(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        PASS = "PASS", "Pass"
        FAIL = "FAIL", "Fail"

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_enrollment", db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name="course_enrollment", db_index=True)
    user_learning_path = models.ForeignKey("UserLearningPath",
                                           on_delete=models.CASCADE,
                                           related_name="user_learning_path")
    course_status = models.CharField(
        max_length=15,
        default=EnrollmentStatusEnum.IN_PROGRESS,
        choices=EnrollmentStatusEnum.choices,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')
        indexes = [
            models.Index(fields=['course_status']),
        ]

    def __str__(self):
        return f"User {self.user.username} in Course {self.course.title}"


class CourseFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_feedback",
                             db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name="course_feedback", db_index=True)
    rating = models.IntegerField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"User {self.user.username} rated {self.rating} for {self.course.title}"


class CourseLearningPath(models.Model):
    learning_path_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name="course_path", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "created_at"

    def __str__(self):
        return str(self.learning_path_id)


class LearningUnit(models.Model):
    learning_unit_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)
    learning_path = models.ForeignKey(CourseLearningPath,
                                      on_delete=models.CASCADE,
                                      related_name="course_learning_unit",
                                      db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='topic_unit',
                              db_index=True)
    order = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.learning_unit_id)


class UserLearningPath(models.Model):
    class StatusEnum(models.TextChoices):
        START = "START", "Start"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETE = "COMPLETE", "Complete"

    user_learning_path_id = models.UUIDField(primary_key=True,
                                             default=uuid.uuid4,
                                             editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_paths",
                             db_index=True)
    learning_path = models.ForeignKey(CourseLearningPath,
                                      on_delete=models.CASCADE,
                                      related_name="user_learning_paths",
                                      db_index=True)
    current_learning_unit = models.ForeignKey(LearningUnit,
                                              on_delete=models.SET_NULL,
                                              null=True, blank=True,
                                              related_name="current_for_users")
    overall_percentage = models.IntegerField(default=0,
                                             validators=[MinValueValidator(0),
                                                         MaxValueValidator(
                                                             100)])
    status = models.CharField(max_length=15, default=StatusEnum.START,
                              choices=StatusEnum.choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.learning_path.course.title}"


class UserLearningUnit(models.Model):
    class AttemptStatusEnum(models.TextChoices):
        START = "START", "Start"
        HALF_COMPLETED = "HALF_COMPLETED", "Half Completed"
        COMPLETE = "COMPLETE", "Complete"

    user_learning_path = models.ForeignKey(UserLearningPath,
                                           on_delete=models.CASCADE,
                                           related_name="learning_units",
                                           db_index=True)
    learning_unit = models.ForeignKey(LearningUnit, on_delete=models.CASCADE,
                                      related_name="user_units", db_index=True)
    is_locked = models.BooleanField(default=True)
    percentage = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=16, choices=AttemptStatusEnum.choices,
                              default=AttemptStatusEnum.START, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['status'])]

    def __str__(self):
        return f"{self.user_learning_path.user.username} - {self.learning_unit.topic.topic_title}"


class Video(models.Model):
    video_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    title = models.CharField(max_length=255)
    topic = models.OneToOneField("Topic", on_delete=models.CASCADE,related_name="topic_video",null=True,blank=True)
    video_url = models.URLField()
    estimated_duration_in_mins = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
