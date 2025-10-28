import pytest
from unittest.mock import Mock
from faker import Faker
import json

Faker.seed(42)

from course_management.interactors.course.get_course_completion_percentage import (
    GetCourseCompletionPercentageInteractor
)
from course_management.exceptions.custom_exceptions import UserNotEnrolledCourse


from tests.factories import ModuleDTOFactory, TopicDTOFactory, TopicProgressDTOFactory


@pytest.fixture(autouse=True)
def reset_factories():
    Faker.seed(0)
    ModuleDTOFactory.reset_sequence(0)
    TopicDTOFactory.reset_sequence(0)
    TopicProgressDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def course_storage():
    s = Mock()
    yield s
    s.reset_mock()


@pytest.fixture
def enrollment_storage():
    s = Mock()
    s.get_user_course_enrollment_exist.return_value = True
    yield s
    s.reset_mock()


@pytest.fixture
def user_storage():
    s = Mock()
    yield s
    s.reset_mock()


@pytest.fixture
def module_storage():
    s = Mock()
    yield s
    s.reset_mock()


@pytest.fixture
def topic_storage():
    s = Mock()
    yield s
    s.reset_mock()


@pytest.fixture
def interactor(course_storage, enrollment_storage, user_storage, module_storage, topic_storage):
    return GetCourseCompletionPercentageInteractor(
        course_storage=course_storage,
        enrollment_storage=enrollment_storage,
        user_storage=user_storage,
        module_storage=module_storage,
        topic_storage=topic_storage
    )


# Tests for get_course_completion_percentage
def test_get_course_completion_percentage_successfully(
        interactor,
        module_storage,
        topic_storage,
        enrollment_storage,
        snapshot
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"

    modules = ModuleDTOFactory.build_batch(2)
    module_storage.get_course_modules.return_value = modules

    topics = TopicDTOFactory.build_batch(3)
    topic_storage.get_topics_for_module_ids.return_value = topics

    topic_progresses = [
        TopicProgressDTOFactory.build(percentage=60),
        TopicProgressDTOFactory.build(percentage=80),
        TopicProgressDTOFactory.build(percentage=100),
    ]
    topic_storage.get_user_topic_progresses.return_value = topic_progresses

    # ACT
    result = interactor.get_course_completion_percentage(user_id=user_id, course_id=course_id)

    # ASSERT
    assert result.percentage == 80
    enrollment_storage.update_course_percentage.assert_called_once_with(
        user_id=user_id, course_id=course_id, course_percentage=80
    )

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps(result.__dict__, sort_keys=True, indent=2),
        "get_course_completion_percentage_snapshot.json"
    )


def test_get_course_completion_percentage_with_zero_progress(
        interactor,
        module_storage,
        topic_storage,
        snapshot
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"

    modules = ModuleDTOFactory.build_batch(1)
    module_storage.get_course_modules.return_value = modules

    topics = TopicDTOFactory.build_batch(3)
    topic_storage.get_topics_for_module_ids.return_value = topics

    topic_storage.get_user_topic_progresses.return_value = []

    # ACT
    result = interactor.get_course_completion_percentage(user_id=user_id, course_id=course_id)

    # ASSERT
    assert result.percentage == 0

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps(result.__dict__, sort_keys=True, indent=2),
        "get_course_completion_percentage_zero_snapshot.json"
    )


# Tests for calculate_user_course_completion_percentage
def test_calculate_user_course_completion_percentage_successfully(
        interactor,
        module_storage,
        topic_storage,
        snapshot
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"

    modules = ModuleDTOFactory.build_batch(2)
    module_storage.get_course_modules.return_value = modules

    topics = TopicDTOFactory.build_batch(4)
    topic_storage.get_topics_for_module_ids.return_value = topics

    topic_progresses = [
        TopicProgressDTOFactory.build(percentage=100),
        TopicProgressDTOFactory.build(percentage=80),
        TopicProgressDTOFactory.build(percentage=60),
        TopicProgressDTOFactory.build(percentage=40),
    ]
    topic_storage.get_user_topic_progresses.return_value = topic_progresses

    # ACT
    result = interactor.calculate_user_course_completion_percentage(
        course_id=course_id, user_id=user_id
    )

    # ASSERT
    assert result == 70

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps({"percentage": result}, sort_keys=True, indent=2),
        "calculate_completion_percentage_snapshot.json"
    )


def test_calculate_user_course_completion_percentage_returns_zero(
        interactor,
        module_storage,
        topic_storage,
        snapshot
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"

    modules = ModuleDTOFactory.build_batch(1)
    module_storage.get_course_modules.return_value = modules

    topics = TopicDTOFactory.build_batch(5)
    topic_storage.get_topics_for_module_ids.return_value = topics

    topic_storage.get_user_topic_progresses.return_value = []

    # ACT
    result = interactor.calculate_user_course_completion_percentage(
        course_id=course_id, user_id=user_id
    )

    # ASSERT
    assert result == 0

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps({"percentage": result}, sort_keys=True, indent=2),
        "calculate_completion_percentage_zero_snapshot.json"
    )


# Tests for _check_user_course_enrollment
def test_check_user_course_enrollment_user_enrolled(
        interactor,
        enrollment_storage
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"

    # ACT (should not raise exception)
    interactor._check_user_course_enrollment(user_id=user_id, course_id=course_id)

    # ASSERT
    enrollment_storage.get_user_course_enrollment_exist.assert_called_once_with(
        course_id=course_id, user_id=user_id
    )


def test_check_user_course_enrollment_raises_exception(
        interactor,
        enrollment_storage,
        snapshot
):
    # ARRANGE
    user_id = "U001"
    course_id = "C001"
    enrollment_storage.get_user_course_enrollment_exist.return_value = False

    # ACT
    with pytest.raises(UserNotEnrolledCourse) as exc:
        interactor._check_user_course_enrollment(user_id=user_id, course_id=course_id)

    # ASSERT
    assert exc.value.user_id == user_id

    # SNAPSHOT
    snapshot.assert_match(
        json.dumps({"user_id": exc.value.user_id}, sort_keys=True, indent=2),
        "check_enrollment_raises_snapshot.json"
    )