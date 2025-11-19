import pytest
from faker import Faker

from course_management.interactors.dtos import LearningPathForCourseDTO
from course_management.storages.learning_path_storage import \
    LearningPathStorage
from course_management.tests.factories.storage_factories import \
    CourseLearningPathFactory, CourseFactory

Faker.seed(1)


class TestLearningPath:

    @pytest.mark.django_db
    def test_learning_path_exist(self):
        learning_path = CourseLearningPathFactory()
        learning_path_storage = LearningPathStorage()
        result = learning_path_storage.learning_path_exist(
            learning_path_id=learning_path.learning_path_id)

        assert result is True

    @pytest.mark.django_db
    def test_create_course_learning_path(self):
        learning_path = CourseLearningPathFactory()
        learning_path_storage = LearningPathStorage()

        result = learning_path_storage.create_course_learning_path(
            course_id=learning_path.course.course_id)

        expected_output = LearningPathForCourseDTO(
            learning_path_id=result.learning_path_id,
            course_id=learning_path.course.course_id,
            course_title=learning_path.course.title,
            total_units=0,
            estimated_total_duration_in_minutes=learning_path.course.estimated_duration_in_min,
            learning_units=[],
        )

        assert result == expected_output

    @pytest.mark.django_db
    def test_get_course_learning_path(self, snapshot):
        # Arrange
        learning_path_id = "12345678-1234-5678-1234-567812345678"

        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345679",
            title="Fixed Course",
            estimated_duration_in_min=120
        )

        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        learning_path_storage = LearningPathStorage()

        # Act
        result = learning_path_storage.get_course_learning_path(
            learning_path_id=learning_path.learning_path_id
        )

        # Assert
        snapshot.assert_match(repr(result), "get_learning_path.txt")

    @pytest.mark.django_db
    def test_get_latest_learning_path_for_course(self, snapshot):
        learning_path_id = "12345678-1234-5678-1234-567812345678"

        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345679",
            title="Fixed Course",
            estimated_duration_in_min=120
        )

        CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        learning_path_storage = LearningPathStorage()

        # Act
        result = learning_path_storage.get_latest_learning_path_by_course_id(
            course_id=course.course_id)

        snapshot.assert_match(repr(result), "get_latest_learning_path.txt")
