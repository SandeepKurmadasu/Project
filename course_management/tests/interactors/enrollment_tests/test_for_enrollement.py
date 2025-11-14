import pytest
from unittest.mock import Mock, patch, create_autospec
from faker import Faker
import json

from course_management.exceptions.custom_exceptions import (
    UserNotFound,
    CourseNotFound,
    CourseInProgressException
)
from course_management.interactors.dtos import EnrollmentStatusEnum
from course_management.interactors.enrollment.enrollment_interactor import \
    EnrollmentInteractor
from course_management.interactors.learning_path.generate_learning_path_for_course import (
    GenerateLearningPathForCourseInteractor
)
from course_management.interactors.storage_interfaces.user_learning_path import (
    UserLearningPathStorageInterface
)

from course_management.tests.factories.interactor_factories import \
    EnrollmentDTOFactory

Faker.seed(42)

@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def course_storage():
    return Mock()


@pytest.fixture
def enrollment_storage():
    s = Mock()
    s.create_enrollment.return_value = EnrollmentDTOFactory.build()
    s.get_user_enrolled_courses.return_value = []
    return s


@pytest.fixture
def user_learning_path_storage():
    return create_autospec(UserLearningPathStorageInterface)


@pytest.fixture
def learning_path_storage():
    return Mock()


@pytest.fixture
def module_storage():
    return Mock()


@pytest.fixture
def topic_storage():
    return Mock()


@pytest.fixture
def learning_unit_storage():
    return Mock()


@pytest.fixture
def interactor(user_storage, course_storage, enrollment_storage,
               user_learning_path_storage, learning_path_storage,
               module_storage, topic_storage, learning_unit_storage):
    return EnrollmentInteractor(
        enrollment_storage=enrollment_storage,
        user_storage=user_storage,
        course_storage=course_storage,
        user_learning_path_storage=user_learning_path_storage,
        learning_path_storage=learning_path_storage,
        module_storage=module_storage,
        topic_storage=topic_storage,
        learning_unit_storage=learning_unit_storage,
    )


class TestEnrollments:

    def test_create_enrollment_successfully(
            self, interactor, user_storage, course_storage, enrollment_storage,
            learning_path_storage, user_learning_path_storage, snapshot):
        user_id = "user123"
        course_id = "C001"

        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = True

        existing_course_lp = Mock(learning_path_id="CLP_EXIST")
        learning_path_storage.get_latest_learning_path_by_course_id.return_value = (
            existing_course_lp
        )

        created_user_lp = Mock(learning_path_id="ULP001")
        user_learning_path_storage.create_user_learning_path.return_value = created_user_lp

        enrollment_storage.check_user_course_enrollment_exist.return_value = False

        enrollment = EnrollmentDTOFactory.build(
            id=1,
            user_id=user_id,
            course_id=course_id,
            course_status=EnrollmentStatusEnum.FAIL
        )
        enrollment_storage.create_enrollment.return_value = enrollment

        result = interactor.enroll_user_in_course(user_id, course_id)

        assert result.id == 1
        snapshot.assert_match(repr(result), "create_enrollment_snapshot.json")

    def test_get_user_enrolled_courses_successfully(
            self, interactor, user_storage, enrollment_storage, snapshot):
        user_id = "user123"

        user_storage.check_user_exists.return_value = True
        enrolled = [
            EnrollmentDTOFactory.build(id=1, user_id=user_id, course_id="C01"),
            EnrollmentDTOFactory.build(id=2, user_id=user_id, course_id="C02"),
        ]
        enrollment_storage.get_user_enrolled_courses.return_value = enrolled

        result = interactor.get_user_enrolled_courses(user_id)
        snapshot.assert_match(repr(result),
                              "get_user_enrolled_courses_snapshot.json")

    def test_user_not_found_create_raises(self, interactor, user_storage,
                                          snapshot):
        user_storage.check_user_exists.return_value = False

        with pytest.raises(UserNotFound) as exc:
            interactor.enroll_user_in_course(user_id="U1", course_id="C1")

        data = {
            "error": str(exc.value),
            "user_id": exc.value.user_id
        }
        snapshot.assert_match(repr(data),
                              "user_not_found_snapshot.json")

    def test_course_not_found_create_raises(
            self, interactor, user_storage, course_storage, snapshot):
        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = False

        with pytest.raises(CourseNotFound) as exc:
            interactor.enroll_user_in_course(user_id="U1", course_id="C999")

        data = {
            "error": str(exc.value),
            "course_id": exc.value.course_id,
        }
        snapshot.assert_match(json.dumps(data, indent=2),
                              "course_not_found_snapshot.json")

    def test_learning_path_created_if_missing(
            self, interactor, user_storage, course_storage,
            learning_path_storage, user_learning_path_storage,
            enrollment_storage, snapshot):
        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = True

        learning_path_storage.get_latest_learning_path_by_course_id.return_value = None

        generated_lp = Mock(learning_path_id="LP_GEN")
        with patch.object(
                GenerateLearningPathForCourseInteractor,
                "generate_learning_path_for_course",
                return_value=generated_lp
        ):
            created_user_lp = Mock(learning_path_id="ULP_NEW")
            user_learning_path_storage.create_user_learning_path.return_value = created_user_lp

            enrollment_storage.check_user_course_enrollment_exist.return_value = False
            enrollment = EnrollmentDTOFactory.build(id=55)
            enrollment_storage.create_enrollment.return_value = enrollment

            result = interactor.enroll_user_in_course("U200", "C200")

            user_learning_path_storage.create_user_learning_path.assert_called_once()

            snapshot.assert_match(repr(result),
                                  "learning_path_created_snapshot.json")

    def test_re_enroll_allowed_when_failed(
            self, interactor, user_storage, course_storage,
            learning_path_storage,
            user_learning_path_storage, enrollment_storage, snapshot):
        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = True

        learning_path_storage.get_latest_learning_path_by_course_id.return_value = Mock(
            learning_path_id="CLP")
        user_learning_path_storage.create_user_learning_path.return_value = Mock(
            learning_path_id="ULP")

        enrollment_storage.check_user_course_enrollment_exist.return_value = True
        enrollment_storage.get_enrollment.return_value = Mock(
            course_status=EnrollmentStatusEnum.FAIL
        )

        new_enrollment = EnrollmentDTOFactory.build(id=33)
        enrollment_storage.create_enrollment.return_value = new_enrollment

        result = interactor.enroll_user_in_course("U10", "C10")

        snapshot.assert_match(repr(result),
                              "re_enroll_after_fail_snapshot.json")

    def test_re_enroll_blocked_when_in_progress(
            self, interactor, user_storage, course_storage,
            learning_path_storage,
            user_learning_path_storage, enrollment_storage):
        user_storage.check_user_exists.return_value = True
        course_storage.check_course_exists.return_value = True

        learning_path_storage.get_latest_learning_path_by_course_id.return_value = Mock(
            learning_path_id="CLP99"
        )
        user_learning_path_storage.create_user_learning_path.return_value = Mock(
            learning_path_id="ULP99"
        )

        enrollment_storage.check_user_course_enrollment_exist.return_value = True
        enrollment_storage.get_enrollment.return_value = Mock(
            course_status=EnrollmentStatusEnum.IN_PROGRESS
        )

        with pytest.raises(CourseInProgressException):
            interactor.enroll_user_in_course("U99", "C99")
