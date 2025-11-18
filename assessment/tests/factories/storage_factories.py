import datetime

import factory
import uuid
from decimal import Decimal
from factory.django import DjangoModelFactory

from assessment.models import Assessment, Attempt, \
    AssessmentAttemptQuestionSubmission


class AssessmentFactory(DjangoModelFactory):
    class Meta:
        model = Assessment

    assessment_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("sentence", nb_words=4)
    icon = factory.Faker("word")
    assessment_type = Assessment.AssessmentType.QUIZ  # default, can be overridden
    description = factory.Faker("paragraph")
    no_of_questions = factory.Faker("random_int", min=1, max=20)
    pass_marks = factory.Faker("random_int", min=0, max=100)
    marks = factory.Faker("random_int", min=0, max=100)
    pass_percentage = factory.Faker("random_int", min=0, max=100)
    easy_count = factory.Faker("random_int", min=0, max=10)
    medium_count = factory.Faker("random_int", min=0, max=10)
    hard_count = factory.Faker("random_int", min=0, max=10)
    attempts_limit = factory.Faker("random_int", min=1, max=5)
    estimated_duration_in_minutes = factory.Faker("random_int", min=10, max=180)


class AttemptFactory(DjangoModelFactory):
    class Meta:
        model = Attempt

    attempt_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory('course_management.factories.UserFactory')
    assessment = factory.SubFactory(AssessmentFactory)
    total_points = Decimal("0.00")
    status = Attempt.AttemptStatusEnum.START
    question_ids = factory.LazyFunction(list)  # empty list by default
    started_at = factory.LazyFunction(
        lambda: datetime.datetime(2025, 11, 18, 13, 21, 51, 922886))


class AssessmentAttemptQuestionSubmissionFactory(DjangoModelFactory):
    class Meta:
        model = AssessmentAttemptQuestionSubmission

    attempt = factory.SubFactory(AttemptFactory)
    question = factory.SubFactory('course_management.factories.QuestionFactory')
    selected_option = factory.Faker("word")
    is_response_correct = AssessmentAttemptQuestionSubmission.Response.WRONG
