import pytest

from course_management.storages.user_learning_path_storage import \
    UserLearningPathStorage
from course_management.tests.factories.storage_factories import UserFactory, \
    CourseFactory, CourseLearningPathFactory, LearningUnitFactory, \
    UserLearningPathFactory


class TestUserLearningPath:

    @pytest.mark.django_db
    def test_get_user_learning_path(self, snapshot):
        # -------------------------
        # Arrange
        # -------------------------
        user = UserFactory(user_id="11111111-1111-1111-1111-111111111111")
        course = CourseFactory(
            course_id="22222222-2222-2222-2222-222222222222")

        learning_path = CourseLearningPathFactory(
            learning_path_id="33333333-3333-3333-3333-333333333333",
            course=course
        )

        current_learning_unit = LearningUnitFactory(
            learning_unit_id="44444444-4444-4444-4444-444444444444",
            learning_path=learning_path
        )

        UserLearningPathFactory(
            user_learning_path_id="55555555-5555-5555-5555-555555555555",
            user=user,
            learning_path=learning_path,
            current_learning_unit=current_learning_unit,
            overall_percentage=75,
            status="IN_PROGRESS",

        )

        storage = UserLearningPathStorage()

        # ACT
        result = storage.get_user_learning_path(
            user_id=user.user_id,
            course_id=course.course_id,
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_user_learning_path.json",
        )

    @pytest.mark.django_db
    def test_get_user_learning_path_with_id(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"

        user = UserFactory(user_id=user_id)
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345128")
        course_learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )
        current_learning_unit = LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345129",
            learning_path=course_learning_path
        )
        UserLearningPathFactory(
            user_learning_path_id="12345678-1234-5678-1234-567812345130",
            user=user,
            learning_path=course_learning_path,
            current_learning_unit=current_learning_unit,
            overall_percentage=60,
            status="IN_PROGRESS",
        )

        storage = UserLearningPathStorage()

        result = storage.get_user_learning_path_with_id(
            user_id=user_id,
            learning_path_id=learning_path_id,
        )

        snapshot.assert_match(repr(result),
                              "test_get_user_learning_path_with_id.txt")

    @pytest.mark.django_db
    def test_create_user_learning_path(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"

        UserFactory(user_id=user_id)
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124"
        )
        course_learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345125",
            learning_path=course_learning_path,
            order=1
        )

        storage = UserLearningPathStorage()

        result = storage.create_user_learning_path(
            user_id=user_id,
            course_learning_path_id=learning_path_id,
        )

        output = f"{result.user_id} - {result.learning_path_id}"
        snapshot.assert_match(repr(output),
                              "test_create_user_learning_path.txt")

    @pytest.mark.django_db
    def test_get_user_learning_path_with_user_learning_path_id(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"
        user_learning_path_id = "12345678-1234-5678-1234-567812345128"

        user = UserFactory(user_id=user_id)
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124")
        course_learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )
        learning_unit = LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345125",
            learning_path=course_learning_path,
            order=1
        )
        UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id,
            user=user,
            learning_path=course_learning_path,
            current_learning_unit=learning_unit,
            overall_percentage=42,
            status="IN_PROGRESS",
        )

        storage = UserLearningPathStorage()

        result = storage.get_user_learning_path_with_user_learning_path_id(
            user_learning_path_id=user_learning_path_id
        )

        snapshot.assert_match(repr(result),
                              "test_get_user_learning_path_with_user_learning_path_id.txt")

    @pytest.mark.django_db
    def test_check_user_learning_path_exists(self):
        user_learning_path_id = "12345678-1234-5678-1234-567812345128"
        non_existing_id = "87654321-4321-8765-4321-876543218765"

        UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id)

        storage = UserLearningPathStorage()

        assert storage.check_user_learning_path_exists(
            user_learning_path_id) is True
        assert storage.check_user_learning_path_exists(
            non_existing_id) is False

    @pytest.mark.django_db
    def test_update_user_learning_path_percentage(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345128"
        user_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"

        user = UserFactory(user_id=user_id)
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124")
        course_learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )
        learning_unit = LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345125",
            learning_path=course_learning_path,
            order=1
        )
        UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id,
            user=user,
            learning_path=course_learning_path,
            current_learning_unit=learning_unit,
            overall_percentage=20,
            status="IN_PROGRESS",
        )

        storage = UserLearningPathStorage()

        updated_percentage = 75
        result = storage.update_user_learning_path_percentage(
            user_learning_path_id=user_learning_path_id,
            percentage=updated_percentage
        )

        snapshot.assert_match(repr(result),
                              "test_update_user_learning_path_percentage.txt")
