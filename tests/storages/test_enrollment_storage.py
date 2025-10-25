import pytest
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.models import Enrollment, Course, User

@pytest.mark.django_db
def test_create_enrollment_storage():
    # ARRANGE
    storage = EnrollmentStorage()


    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course = Course.objects.create(
        title='Python',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )

    # ACT
    result = storage.create_enrollment(user_id=str(user.user_id), course_id=str(course.course_id))

    # ASSERT
    assert result.user_id == str(user.user_id)
    assert result.course_id == str(course.course_id)
    assert result.course_percentage == 0
    assert Enrollment.objects.filter(user_id=user.user_id, course_id=course.course_id).exists()


@pytest.mark.django_db
def test_get_user_enrolled_courses_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course1 = Course.objects.create(title='Python', description='Desc', category='Prog', level='BEGINNER')
    course2 = Course.objects.create(title='Django', description='Desc', category='Prog', level='INTERMEDIATE')

    Enrollment.objects.create(user=user, course=course1, course_percentage=50)
    Enrollment.objects.create(user=user, course=course2, course_percentage=75)

    # ACT
    result = storage.get_user_enrolled_courses(user_id=str(user.user_id))

    # ASSERT
    assert len(result) == 2
    assert str(course1.course_id) in result
    assert str(course2.course_id) in result


@pytest.mark.django_db
def test_get_user_enrolled_courses_empty_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    # ACT
    result = storage.get_user_enrolled_courses(user_id='nonexistent_user')

    # ASSERT
    assert len(result) == 0
    assert result == []


@pytest.mark.django_db
def test_update_course_percentage_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course = Course.objects.create(title='Python', description='Desc', category='Prog', level='BEGINNER')
    enrollment = Enrollment.objects.create(user=user, course=course, course_percentage=0)

    # ACT
    result = storage.update_course_percentage(
        user_id=str(user.user_id),
        course_id=str(course.course_id),
        percentage=75
    )

    # ASSERT
    assert result.course_percentage == 75
    enrollment.refresh_from_db()
    assert enrollment.course_percentage == 75


@pytest.mark.django_db
def test_get_user_enrollments_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    # Create test data
    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course1 = Course.objects.create(title='Python', description='Desc', category='Prog', level='BEGINNER')
    course2 = Course.objects.create(title='Django', description='Desc', category='Prog', level='INTERMEDIATE')

    Enrollment.objects.create(user=user, course=course1, course_percentage=50)
    Enrollment.objects.create(user=user, course=course2, course_percentage=75)

    # ACT
    result = storage.get_user_enrollments(user_id=str(user.user_id))

    # ASSERT
    assert len(result) == 2
    assert result[0].user_id == str(user.user_id)
    assert result[1].user_id == str(user.user_id)

    result_course_ids = [r.course_id for r in result]
    assert str(course1.course_id) in result_course_ids
    assert str(course2.course_id) in result_course_ids

    result_percentages = [r.course_percentage for r in result]
    assert 50 in result_percentages
    assert 75 in result_percentages


@pytest.mark.django_db
def test_get_user_enrollments_empty_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    # ACT
    result = storage.get_user_enrollments(user_id='nonexistent_user')

    # ASSERT
    assert len(result) == 0
    assert result == []


@pytest.mark.django_db
def test_get_user_course_enrollment_exist_true_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course = Course.objects.create(title='Python', description='Desc', category='Prog', level='BEGINNER')
    Enrollment.objects.create(user=user, course=course, course_percentage=50)

    # ACT
    result = storage.get_user_course_enrollment_exist(
        course_id=str(course.course_id),
        user_id=str(user.user_id)
    )

    # ASSERT
    assert result is True


@pytest.mark.django_db
def test_get_user_course_enrollment_exist_false_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    user = User.objects.create(
        name='Test User',
        username='testuser',
        password='test123',
        email='test@example.com',
        phone_number=1234567890
    )
    course = Course.objects.create(title='Python', description='Desc', category='Prog', level='BEGINNER')

    # ACT
    result = storage.get_user_course_enrollment_exist(
        course_id=str(course.course_id),
        user_id=str(user.user_id)
    )

    # ASSERT
    assert result is False


@pytest.mark.django_db
def test_get_user_course_enrollment_exist_invalid_ids_storage():
    # ARRANGE
    storage = EnrollmentStorage()

    # ACT
    result = storage.get_user_course_enrollment_exist(
        course_id='invalid_course_id',
        user_id='invalid_user_id'
    )

    # ASSERT
    assert result is False