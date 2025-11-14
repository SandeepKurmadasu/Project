from datetime import timezone, datetime

import factory

from assessment.interactors.dtos import CreateAssessmentDTO, \
    AssessmentDTO, QuestionDTO, \
    AssessmentAttemptDTO, AssessmentTypeEnum
from course_management.interactors.dtos import StatusEnum


class QuestionDTOFactory(factory.Factory):
    class Meta:
        model = QuestionDTO

    question_id = factory.Sequence(lambda n: f"q-{n + 1}")
    question_text = factory.Faker("sentence", nb_words=8)
    question_type = factory.Iterator(["MCQ", "TRUE_FALSE", "FILL_BLANK"])
    difficulty_level = factory.Iterator(["EASY", "MEDIUM", "HARD"])

    options = factory.LazyFunction(
        lambda: [
            {"option_id": "opt-1", "text": "Option A"},
            {"option_id": "opt-2", "text": "Option B"},
            {"option_id": "opt-3", "text": "Option C"},
            {"option_id": "opt-4", "text": "Option D"},
        ]
    )

    correct_answer = factory.LazyFunction(lambda: "opt-2")


class CreateAssessmentDTOFactory(factory.Factory):
    class Meta:
        model = CreateAssessmentDTO

    assessment_title = factory.Faker("word")
    description = factory.Faker("word")
    icon = factory.Faker("word")
    assessment_type = factory.Iterator(list(AssessmentTypeEnum))
    pass_percentage = factory.Faker("random_int", min=0, max=100)
    easy_count = factory.Faker("random_int", min=0, max=10)
    medium_count = factory.Faker("random_int", min=0, max=10)
    no_of_questions = factory.Faker("random_int", min=3, max=20)
    hard_count = factory.Faker("random_int", min=0, max=10)
    estimate_duration_in_mins = factory.Faker("random_int", min=10, max=60)
    attempts_limit = factory.Faker("random_int", min=1, max=5)


class AssessmentDTOFactory(CreateAssessmentDTOFactory):
    class Meta:
        model = AssessmentDTO

    assessment_id = factory.Faker("uuid4")
    marks = factory.Faker("random_int", min=10, max=50)
    pass_marks = factory.Faker("random_int", min=7,max=50)




class AssessmentAttemptDTOFactory(factory.Factory):
    class Meta:
        model = AssessmentAttemptDTO

    attempt_id = factory.Faker("uuid4")
    user_id = factory.Faker("uuid4")
    question_ids = factory.LazyFunction(lambda: [factory.Faker("uuid4") for _ in range(3)])
    assessment_id = factory.Faker("uuid4")
    total_points = factory.Faker("random_int", min=0, max=100)
    status = factory.Iterator(list(StatusEnum))
    started_at = datetime(2025, 11, 2, 12, 0, 0, tzinfo=timezone.utc)
