import pytest

from course_management.models import Enrollment
from course_management.storages.enrollment_storage import EnrollmentStorage
from course_management.tests.factories.storage_factories import \
    EnrollmentFactory, UserFactory, CourseFactory, UserLearningPathFactory, \
    CourseLearningPathFactory


class TestEnrollment:

    @pytest.mark.django_db
    def test_user_course_enrollment(self, snapshot):
        course_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user_learning_path_id = "12345678-1234-5678-1234-567812345690"
        learning_path_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        course = CourseFactory(course_id=course_id, title="Course_title")
        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id, user=user,
            learning_path=learning_path)

        EnrollmentFactory(user=user, course=course,
                          user_learning_path=user_learning_path)
        enrollment_storage = EnrollmentStorage()

        result = enrollment_storage.check_user_course_enrollment_exist(
            user_id=user_id, course_id=course_id)

        snapshot.assert_match(repr(result),
                              "test_check_user_course_enrollment.txt")

    @pytest.mark.django_db
    def test_user_enrolled_courses(self, snapshot):
        course_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user_learning_path_id = "12345678-1234-5678-1234-567812345690"
        learning_path_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        course = CourseFactory(course_id=course_id, title="Course_title")
        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id, user=user,
            learning_path=learning_path)

        EnrollmentFactory(user=user, course=course,
                          user_learning_path=user_learning_path)
        enrollment_storage = EnrollmentStorage()

        result = enrollment_storage.get_user_enrolled_courses(user_id=user_id)

        snapshot.assert_match(repr(result),
                              "test_get_user_enrollment_courses.txt")

    @pytest.mark.django_db
    def test_create_enrollment(self, snapshot):
        course_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user_learning_path_id = "12345678-1234-5678-1234-567812345690"
        learning_path_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        course = CourseFactory(course_id=course_id, title="Course_title")
        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id, user=user,
            learning_path=learning_path)

        enrollment_storage = EnrollmentStorage()

        result = enrollment_storage.create_enrollment(user_id=user_id,
                                                      course_id=course_id,
                                                      user_learning_path_id=user_learning_path_id)

        snapshot.assert_match(repr(result),
                              "test_create_enrollment_course.txt")

    @pytest.mark.django_db
    def test_update_course_percentage(self,snapshot):

        user_id = "12345678-1234-5678-1234-567812345679"
        course_id = "12345678-1234-5678-1234-567812345678"
        learning_path_id = "12345678-1234-5678-1234-567812345680"

        user_learning_path_id = "12345678-1234-5678-1234-567812345690"

        user = UserFactory(user_id=user_id)
        course = CourseFactory(course_id=course_id)
        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)
        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id,
            user=user,
            learning_path=learning_path
        )

        EnrollmentFactory(
            user=user,
            course=course,
            user_learning_path=user_learning_path,
            course_status=Enrollment.EnrollmentStatusEnum.IN_PROGRESS
        )

        storage = EnrollmentStorage()
        new_percentage = 75

        # Act
        result = storage.update_course_percentage(
            user_id=user_id,
            course_id=course_id,
            percentage=new_percentage
        )

        snapshot.assert_match(repr(result),"test_update_percentage.txt")

    @pytest.mark.django_db
    def test_get_enrollment(self, snapshot):
        course_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user_learning_path_id = "12345678-1234-5678-1234-567812345690"
        learning_path_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        course = CourseFactory(course_id=course_id, title="Course_title")
        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id, user=user,
            learning_path=learning_path)

        EnrollmentFactory(user=user, course=course,
                          user_learning_path=user_learning_path)
        enrollment_storage = EnrollmentStorage()

        result = enrollment_storage.get_enrollment(
            user_id=user_id, course_id=course_id)

        snapshot.assert_match(repr(result),
                              "test_get_enrollment.txt")
