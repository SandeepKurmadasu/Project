import pytest
from unittest.mock import Mock
from faker import Faker
import json
from course_management.interactors.course.get_topics_for_course import GetTopicsForCourseInteractor
from course_management.exceptions.custom_exceptions import CourseNotFound
from course_management.tests.factories import ModuleDTOFactory, TopicDTOFactory

@pytest.fixture(autouse=True)
def reset_factories():
    Faker.seed(0)
    ModuleDTOFactory.reset_sequence(0)
    TopicDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def course_storage():
    s = Mock()
    s.check_course_exists.return_value = False
    return s


@pytest.fixture
def module_storage():
    s = Mock()
    s.get_course_modules.return_value = []
    return s


@pytest.fixture
def topic_storage():
    s = Mock()
    s.get_topics_for_module_ids.return_value = []
    return s


@pytest.fixture
def interactor(course_storage, module_storage, topic_storage):
    return GetTopicsForCourseInteractor(
        course_storage=course_storage,
        module_storage=module_storage,
        topic_storage=topic_storage
    )


def test_get_topics_for_course_successfully(interactor, course_storage, module_storage, topic_storage,snapshot):
    # Arrange
    course_id = "C0001"
    modules = [
        ModuleDTOFactory(module_id="M0001", course_id=course_id, module_title="Module-1", estimated_duration=60),
        ModuleDTOFactory(module_id="M0002", course_id=course_id, module_title="Module-2", estimated_duration=90),
    ]
    topics = [
        TopicDTOFactory(topic_id="T0001", module_id="M0001"),
        TopicDTOFactory(topic_id="T0002", module_id="M0002"),
    ]
    course_storage.check_course_exists.return_value = True  # Course exists
    module_storage.get_course_modules.return_value = modules
    topic_storage.get_topics_for_module_ids.return_value = topics

    # Act
    result = interactor.get_topics_for_course(course_id)

    # Assert
    assert len(result) == 2
    assert result[0].topic_id == "T0001"
    assert result[1].topic_id == "T0002"
    topic_storage.get_topics_for_module_ids.assert_called_once_with(module_ids=["M0001", "M0002"])

    #snapshot
    snapshot.assert_match(
        result,
        "topics_for_course_snapshot.json"
    )


def test_course_not_found_raises(interactor, course_storage, module_storage, topic_storage,snapshot):
    # Arrange
    course_id = "C9999"
    course_storage.check_course_exists.return_value = False

    # Act
    with pytest.raises(CourseNotFound) as exc:
        interactor.get_topics_for_course(course_id)

    # Assert
    assert exc.value.course_id == "C9999"

     #snapshot
    snapshot.assert_match(
        exc.value.course_id,
        "course_not_found_snapshot.json"
    )
