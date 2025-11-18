import factory
from assessment.models import Assessment


class AssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assessment

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
