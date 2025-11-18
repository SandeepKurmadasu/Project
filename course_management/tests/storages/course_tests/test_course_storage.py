import json
import pytest
import uuid

from course_management.interactors.dtos import (
    CreateCourseDTO,
    UpdateCourseDTO,
    CourseCategoryEnum,
    LevelEnum,
)
from course_management.models import Course
from course_management.storages.course_storage import CourseStorage


CID1 = uuid.UUID("11111111-1111-1111-1111-111111111111")
CID2 = uuid.UUID("22222222-2222-2222-2222-222222222222")
CID3 = uuid.UUID("33333333-3333-3333-3333-333333333333")


@pytest.mark.django_db
def test_get_courses(snapshot):

    Course.objects.create(
        course_id=CID1,
        title="Python",
        description="Learn",
        category="DEV",
        level="BEGINNER",
        average_rating=4.2,
        estimated_duration_in_min=120,
    )

    storage = CourseStorage()
    result = storage.get_courses([str(CID1)])

    snapshot.assert_match(
        json.dumps(
            [{**r.__dict__, "course_id": str(r.course_id)} for r in result],
            sort_keys=True,
            indent=2,
        ),
        "get_courses.json",
    )


@pytest.mark.django_db
def test_get_valid_course_ids(snapshot):

    Course.objects.create(
        course_id=CID2,
        title="Course X",
        description="Desc",
        category="DEV",
        level="BEGINNER",
        estimated_duration_in_min=10,
    )

    storage = CourseStorage()
    result = storage.get_valid_course_ids([str(CID2)])

    snapshot.assert_match(
        json.dumps(result, sort_keys=True, indent=2),
        "get_valid_course_ids.json",
    )


@pytest.mark.django_db
def test_create_courses(snapshot):

    dto = CreateCourseDTO(
        title="New Course",
        description="Learning",
        category=CourseCategoryEnum.DEVELOPMENT,
        level=LevelEnum.BEGINNER,
    )

    storage = CourseStorage()
    result = storage.create_courses([dto])

    normalized = []
    for r in result:
        d = r.__dict__.copy()
        d["course_id"] = "ANY_UUID"
        normalized.append(d)

    snapshot.assert_match(
        json.dumps(normalized, sort_keys=True, indent=2),
        "create_courses.json",
    )

@pytest.mark.django_db
def test_update_courses(snapshot):

    Course.objects.create(
        course_id=CID1,
        title="Old",
        description="Old Desc",
        category="DEV",
        level="BEGINNER",
        average_rating=3.0,
        estimated_duration_in_min=50,
    )

    dto = UpdateCourseDTO(
        course_id=str(CID1),
        title="New Title",
        description="New Desc",
        category=CourseCategoryEnum.DESIGN,
        level=LevelEnum.INTERMEDIATE,
    )

    storage = CourseStorage()
    result = storage.update_courses([dto])

    snapshot.assert_match(
        json.dumps(
            [{**r.__dict__, "course_id": str(r.course_id)} for r in result],
            sort_keys=True,
            indent=2,
        ),
        "update_courses.json",
    )


@pytest.mark.django_db
def test_check_course_exists(snapshot):

    Course.objects.create(
        course_id=CID3,
        title="Exists",
        description="X",
        category="DEV",
        level="BEGINNER",
        estimated_duration_in_min=5,
    )

    storage = CourseStorage()
    result = storage.check_course_exists(str(CID3))

    snapshot.assert_match(
        json.dumps(result, sort_keys=True, indent=2),
        "check_course_exists.json",
    )


@pytest.mark.django_db
def test_get_all_courses(snapshot):

    Course.objects.create(
        course_id=CID1,
        title="C1",
        description="D1",
        category="DEV",
        level="BEGINNER",
        average_rating=4.0,
        estimated_duration_in_min=60,
    )

    storage = CourseStorage()
    result = storage.get_all_courses()

    snapshot.assert_match(
        json.dumps(
            [{**r.__dict__, "course_id": str(r.course_id)} for r in result],
            sort_keys=True,
            indent=2,
        ),
        "get_all_courses.json",
    )


@pytest.mark.django_db
def test_get_course_ids_by_title(snapshot):

    Course.objects.create(
        course_id=CID2,
        title="Python",
        description="D",
        category="DEV",
        level="BEGINNER",
        estimated_duration_in_min=10,
    )

    storage = CourseStorage()
    result = storage.get_course_ids_by_title(["Python"])

    snapshot.assert_match(
        json.dumps(result, sort_keys=True, indent=2),
        "get_course_ids_by_title.json",
    )


@pytest.mark.django_db
def test_update_course_rating(snapshot):

    Course.objects.create(
        course_id=CID1,
        title="Rating",
        description="Desc",
        category="DEV",
        level="BEGINNER",
        average_rating=3.0,
        estimated_duration_in_min=40,
    )

    storage = CourseStorage()
    result = storage.update_course_rating(str(CID1), 4.5)

    snapshot.assert_match(
        json.dumps(
            {**result.__dict__, "course_id": str(result.course_id)},
            sort_keys=True,
            indent=2,
        ),
        "update_course_rating.json",
    )
