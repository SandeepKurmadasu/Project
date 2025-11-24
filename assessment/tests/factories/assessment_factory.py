import factory
from assessment.models import Assessment


class AssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assessment

    assessment_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    title = "Sample Assessment"
    icon = "icon.png"
    assessment_type = Assessment.AssessmentType.QUIZ
    description = "Sample description"
    no_of_questions = 10
    pass_marks = 5
    marks = 10
    pass_percentage = 50
    easy_count = 2
    medium_count = 5
    hard_count = 3
    attempts_limit = 1
    estimated_duration_in_minutes = 30
