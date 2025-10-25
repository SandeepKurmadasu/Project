import pytest
from course_management.interactors.dtos import CreateCourseDTO, UpdateCourseDTO
from course_management.storages.course_storage import CourseStorage
from course_management.models import Course

@pytest.mark.django_db
def test_create_courses_storage():
    # ARRANGE
    storage = CourseStorage()
    input_courses = [
        CreateCourseDTO(title="Python", description="Learn Python", category="Programming", level="BEGINNER"),
        CreateCourseDTO(title="Django", description="Learn Django", category="Programming", level="INTERMEDIATE")
    ]

    # ACT
    result = storage.create_courses(input_courses)

    # ASSERT
    assert len(result) == 2
    assert Course.objects.count() == 2
    assert result[0].title == "Python"
    assert result[1].title == "Django"

@pytest.mark.django_db
def test_get_courses_storage():
    # ARRANGE
    storage = CourseStorage()
    course1 = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")
    course2 = Course.objects.create(title="Django", description="Web", category="Prog", level="INTERMEDIATE")

    # ACT
    result = storage.get_courses([str(course1.course_id), str(course2.course_id)])

    # ASSERT
    assert len(result) == 2
    result_ids = [r.course_id for r in result]
    assert str(course1.course_id) in result_ids
    assert str(course2.course_id) in result_ids


@pytest.mark.django_db
def test_update_courses_storage():
    # ARRANGE
    storage = CourseStorage()
    course = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")

    updated_data = [UpdateCourseDTO(
        course_id=str(course.course_id),
        title="Python 3",
        description="Updated Desc",
        category="Programming",
        level="BEGINNER"
    )]

    # ACT
    result = storage.update_courses(updated_data)

    # ASSERT
    assert result[0].title == "Python 3"
    course.refresh_from_db()
    assert course.title == "Python 3"

@pytest.mark.django_db
def test_get_valid_course_ids_storage():
    # ARRANGE
    storage = CourseStorage()
    course1 = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")
    course2 = Course.objects.create(title="Django", description="Web", category="Prog", level="INTERMEDIATE")

    # ACT
    valid_ids = storage.get_valid_course_ids([str(course1.course_id), "invalid_id"])

    # ASSERT
    assert valid_ids == [str(course1.course_id)]

@pytest.mark.django_db
def test_check_course_exists_storage():
    # ARRANGE
    storage = CourseStorage()
    course = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")

    # ACT & ASSERT
    assert storage.check_course_exists(str(course.course_id)) is True
    assert storage.check_course_exists("invalid_id") is False

@pytest.mark.django_db
def test_get_all_course_ids_storage():
    # ARRANGE
    storage = CourseStorage()
    c1 = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")
    c2 = Course.objects.create(title="Django", description="Web", category="Prog", level="INTERMEDIATE")

    # ACT
    result = storage.get_all_course_ids()

    # ASSERT
    assert str(c1.course_id) in result
    assert str(c2.course_id) in result

@pytest.mark.django_db
def test_get_recommend_courses_storage():
    # ARRANGE
    storage = CourseStorage()
    c1 = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")
    c2 = Course.objects.create(title="Django", description="Web", category="Prog", level="INTERMEDIATE")

    # ACT
    result = storage.get_recommend_courses([str(c1.course_id)])

    # ASSERT
    assert len(result) == 1
    assert result[0].course_id == str(c1.course_id)

@pytest.mark.django_db
def test_get_title_course_ids_storage():
    # ARRANGE
    storage = CourseStorage()
    c1 = Course.objects.create(title="Python", description="Desc", category="Prog", level="BEGINNER")

    # ACT
    result = storage.get_title_course_ids(["Python", "Django"])

    # ASSERT
    assert result == [str(c1.course_id)]
