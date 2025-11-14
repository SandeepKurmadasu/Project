import pytest
from unittest.mock import Mock, create_autospec
from faker import Faker

from course_management.exceptions.custom_exceptions import \
    UserNotFound, \
    CourseNotFound
from course_management.interactors.dtos import \
    EnrollmentStatusEnum
from course_management.interactors.enrollment.enrollment_interactor import \
    EnrollmentInteractor
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.tests.factories.interactor_factories import \
    EnrollmentDTOFactory

Faker.seed(42)
import json


@pytest.fixture
def user_storage():
    s = Mock()
    s.check_user_exists.return_value = False
    return s


@pytest.fixture
def course_storage():
    s = Mock()
    s.check_course_exists.return_value = False
    return s


@pytest.fixture
def enrollment_storage():
    s = Mock()
    s.create_enrollment.return_value = EnrollmentDTOFactory.build()
    s.get_user_enrolled_courses.return_value = []
    return s


@pytest.fixture
def interactor(user_storage, course_storage, enrollment_storage):
    return EnrollmentInteractor(
        user_storage=user_storage,
        course_storage=course_storage,
        enrollment_storage=enrollment_storage,
        user_learning_path_storage=create_autospec(
            UserLearningPathStorageInterface)
    )


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EnrollmentStatusEnum):
            return obj.value
        return super().default(obj)


class TestEnrollments:

    def test_create_enrollment_successfully(self, interactor, user_storage,
                                            course_storage,
                                            enrollment_storage, snapshot):
        EnrollmentDTOFactory.reset_sequence(0)
        user_id = "user123"
        course_id = "C0001"
        user_learning_path_id = "ULP1"
        enrollment = EnrollmentDTOFactory.build(
            id=1,
            user_id=user_id,
            course_id=course_id,
            course_status=EnrollmentStatusEnum.FAIL,
            course_percentage=50
        )

        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = True

        enrollment_storage.get_enrollment.return_value = None

        enrollment_storage.create_enrollment.return_value = enrollment

        # Act
        result = interactor.enroll_user_in_course(user_id=user_id,
                                             course_id=course_id,
                                             user_learning_path_id=user_learning_path_id)

        # Assert
        assert result.id == 1
        assert result.user_id == user_id
        assert result.course_id == course_id
        assert result.course_percentage == 50
        enrollment_storage.create_enrollment.assert_called_once_with(
            user_id=user_id,
            course_id=course_id)

        # Snapshot
        snapshot.assert_match(
            json.dumps(result.__dict__, sort_keys=True, indent=2,
                       cls=EnumEncoder),
            "create_enrollment_snapshot.json"
        )

    def test_get_user_enrolled_courses_successfully(self, interactor,
                                                    user_storage,
                                                    enrollment_storage,
                                                    snapshot):
        # Arrange
        user_id = "user123"
        enrolled_courses = [
            EnrollmentDTOFactory.build(id=1, user_id=user_id,
                                       course_id="C0001",
                                       course_percentage=50),
            EnrollmentDTOFactory.build(id=2, user_id=user_id,
                                       course_id="C0002",
                                       course_percentage=75),
        ]
        user_storage.check_user_exists.return_value = True
        enrollment_storage.get_user_enrolled_courses.return_value = enrolled_courses

        # Act
        result = interactor.get_user_enrolled_courses(user_id)

        # Assert
        assert len(result) == 2
        assert result[0].user_id == user_id
        assert result[1].course_id == "C0002"
        enrollment_storage.get_user_enrolled_courses.assert_called_once_with(
            user_id=user_id)

        # snapshot
        snapshot.assert_match(
            repr(result),
            "get_user_enrolled_courses_snapshot.json"
        )

    @pytest.mark.parametrize("invalid_user_id", [None, ""])
    def test_user_not_found_create_raises(self, interactor, user_storage,
                                          course_storage,
                                          enrollment_storage, invalid_user_id,
                                          snapshot):
        # Arrange
        user_id = "user999"
        course_id = "C0001"
        user_learning_path_id = "ULP1"
        user_storage.check_user_exists.return_value = False

        # Act
        with pytest.raises(UserNotFound) as exc:
            interactor.enroll_user_in_course(user_id=user_id,
                                             course_id=course_id,
                                             user_learning_path_id=user_learning_path_id)

        # Assert
        assert exc.value.user_id == user_id

        # snapshot
        snapshot.assert_match(
            json.dumps({"error": str(exc.value), "user_id": exc.value.user_id},
                       sort_keys=True, indent=2),
            f"user_not_found_create_{invalid_user_id}_snapshot.json"
        )

    def test_course_not_found_create_raises(self, interactor, user_storage,
                                            course_storage,
                                            enrollment_storage, snapshot):
        # Arrange
        user_id = "user123"
        course_id = "C9999"
        user_learning_path_id = "ULP1"
        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = False

        # Act
        with pytest.raises(CourseNotFound) as exc:
            interactor.enroll_user_in_course(user_id=user_id,
                                             course_id=course_id,
                                             user_learning_path_id=user_learning_path_id)

        # Assert
        assert exc.value.course_id == course_id

        # snapshot
        snapshot.assert_match(
            json.dumps(
                {"error": str(exc.value), "course_id": exc.value.course_id},
                sort_keys=True, indent=2),
            "course_not_found_create_snapshot.json"
        )

    def test_user_not_found_get_raises(self, interactor, user_storage,
                                       enrollment_storage,
                                       snapshot):
        # Arrange
        user_id = "user999"
        user_storage.check_user_exists.return_value = False

        # Act
        with pytest.raises(UserNotFound) as exc:
            interactor.get_user_enrolled_courses(user_id)

        # Assert
        assert exc.value.user_id == user_id

        # snapshot
        snapshot.assert_match(
            json.dumps({"error": str(exc.value), "user_id": exc.value.user_id},
                       sort_keys=True, indent=2),
            "user_not_found_get_snapshot.json"
        )
