import json
import pytest

from course_management.storages.feedback_storage import FeedbackStorage
from course_management.interactors.dtos import CourseFeedbackDTO
from course_management.models import User, Course, CourseFeedback


def normalize(dto: CourseFeedbackDTO):
    data = dto.__dict__.copy()
    data["user_id"] = "USER-ID"
    data["course_id"] = "COURSE-ID"
    return data


@pytest.mark.django_db
def test_create_course_feedback(snapshot):
    user = User.objects.create(
        name="Baba",
        username="Baba123",
        password="pass",
        gender="MALE",
        email="baba@example.com",
        phone_number=9999,
    )

    course = Course.objects.create(
        title="Python Course",
        description="Basics",
        category="DEV",
        level="BEGINNER",
        estimated_duration_in_min=60,
    )

    dto = CourseFeedbackDTO(
        user_id=str(user.user_id),
        course_id=str(course.course_id),
        rating=5,
        message="Very good!",
    )

    storage = FeedbackStorage()
    result = storage.create_course_feedback(dto)

    snapshot.assert_match(
        json.dumps(normalize(result), sort_keys=True, indent=2),
        "create_feedback",
    )

    assert CourseFeedback.objects.count() == 1
    feedback = CourseFeedback.objects.first()
    assert feedback.rating == 5
    assert feedback.message == "Very good!"


@pytest.mark.django_db
def test_get_course_rating(snapshot):

    user = User.objects.create(
        name="Sandy",
        username="Sandy123",
        password="pass",
        gender="FEMALE",
        email="sandy@example.com",
        phone_number=1111,
    )

    course = Course.objects.create(
        title="Django Course",
        description="Web Dev",
        category="DEV",
        level="ADVANCED",
        estimated_duration_in_min=90,
    )

    CourseFeedback.objects.create(
        user=user,
        course=course,
        rating=4,
        message="Good course"
    )

    CourseFeedback.objects.create(
        user=user,
        course=course,
        rating=3,
        message="Average"
    )

    storage = FeedbackStorage()
    result = storage.get_course_rating(str(course.course_id))


    snapshot.assert_match(
        json.dumps([normalize(r) for r in result], sort_keys=True, indent=2),
        "get_course_rating",
    )

    assert len(result) == 2
    assert result[0].rating in [3, 4]
    assert result[1].rating in [3, 4]
