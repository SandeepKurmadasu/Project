import uuid
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from course_management.models import (
    Course, Module, Topic, User, Enrollment, CourseFeedback,
    CourseLearningPath, LearningUnit, UserLearningPath, UserLearningUnit, Video
)

faker = Faker()
faker.seed_instance(1)



class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    course_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    category = Course.CourseCategoryEnum.DEVELOPMENT
    level = Course.LevelEnum.BEGINNER
    average_rating = 0.0
    estimated_duration_in_min = 120


class ModuleFactory(DjangoModelFactory):
    class Meta:
        model = Module

    module_id = factory.LazyFunction(uuid.uuid4)
    course = factory.SubFactory(CourseFactory)
    module_title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    order = factory.Sequence(lambda n: n+1)
    estimated_duration_in_min = 45


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    topic_id = factory.LazyFunction(uuid.uuid4)
    module = factory.SubFactory(ModuleFactory)
    topic_title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    topic_type = Topic.TopicTypeEnum.LEARNING
    content = factory.Faker("text")
    order = factory.Sequence(lambda n: n)
    estimated_duration_in_mins = 15


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    user_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    username = factory.Faker("user_name")
    gender = User.GenderEnum.MALE
    password = "test123"
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    is_active = True
    otp_count = 0


class CourseLearningPathFactory(DjangoModelFactory):
    class Meta:
        model = CourseLearningPath

    learning_path_id = factory.LazyFunction(uuid.uuid4)
    course = factory.SubFactory(CourseFactory)


class LearningUnitFactory(DjangoModelFactory):
    class Meta:
        model = LearningUnit

    learning_unit_id = factory.LazyFunction(uuid.uuid4)
    learning_path = factory.SubFactory(CourseLearningPathFactory)
    topic = factory.SubFactory(TopicFactory)
    order = factory.Sequence(lambda n: n)


class UserLearningPathFactory(DjangoModelFactory):
    class Meta:
        model = UserLearningPath

    user_learning_path_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    learning_path = factory.SubFactory(CourseLearningPathFactory)
    current_learning_unit = None
    overall_percentage = 0
    status = UserLearningPath.StatusEnum.START


class UserLearningUnitFactory(DjangoModelFactory):
    class Meta:
        model = UserLearningUnit

    user_learning_path = factory.SubFactory(UserLearningPathFactory)
    learning_unit = factory.SubFactory(LearningUnitFactory)
    is_locked = True
    percentage = 0
    status = UserLearningUnit.AttemptStatusEnum.START


class EnrollmentFactory(DjangoModelFactory):
    class Meta:
        model = Enrollment

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    user_learning_path = factory.SubFactory(UserLearningPathFactory)
    course_status = Enrollment.EnrollmentStatusEnum.IN_PROGRESS


class CourseFeedbackFactory(DjangoModelFactory):
    class Meta:
        model = CourseFeedback

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    rating = 5
    message = factory.Faker("sentence")


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    video_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("sentence")
    topic_id = factory.SubFactory(TopicFactory)
    video_url = factory.Faker("url")
    estimated_duration_in_mins = 10
