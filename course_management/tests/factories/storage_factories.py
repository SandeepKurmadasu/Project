import uuid

import factory
from factory.django import DjangoModelFactory

from course_management.models import Course, CourseLearningPath


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    course_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: f"Course {n}")
    description = "Test description"
    category = Course.CourseCategoryEnum.DEVELOPMENT
    level = Course.LevelEnum.BEGINNER
    average_rating = 4.5
    estimated_duration_in_min = 120


class CourseLearningPathFactory(DjangoModelFactory):
    class Meta:
        model = CourseLearningPath

    learning_path_id = factory.LazyFunction(uuid.uuid4)
    course = factory.SubFactory(CourseFactory)