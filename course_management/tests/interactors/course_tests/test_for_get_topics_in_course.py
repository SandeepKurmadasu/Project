import pytest
from unittest.mock import Mock
from faker import Faker

from course_management.exceptions.custom_exceptions import \
    CourseNotFound
from course_management.interactors.course.get_topics_for_course import \
    GetTopicsForCourseInteractor
from course_management.interactors.dtos import TopicTypeEnum
from course_management.tests.factories.interactor_factories import \
    ModuleDTOFactory, TopicDTOFactory

Faker.seed(42)
import json


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
    s.get_topics_with_module_ids.return_value = []
    return s


@pytest.fixture
def interactor(course_storage, module_storage, topic_storage):
    return GetTopicsForCourseInteractor(
        course_storage=course_storage,
        module_storage=module_storage,
        topic_storage=topic_storage
    )


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TopicTypeEnum):
            return obj.value
        return super().default(obj)


class TestGetTopicsInCourse:

    def test_get_topics_for_course_successfully(self, interactor,
                                                course_storage,
                                                module_storage, topic_storage,
                                                snapshot):
        ModuleDTOFactory.reset_sequence(0)
        TopicDTOFactory.reset_sequence(0)

        # Arrange
        course_id = "C0001"
        modules = [
            ModuleDTOFactory(module_id="M0001", course_id=course_id,
                             description="With win man maintain car interesting cost night. Course option human scientist agent poor. Gun finally west around million firm.Gun drop though. Stay address win.",
                             module_title="Module-1", estimated_duration=60),
            ModuleDTOFactory(module_id="M0002", course_id=course_id,
                             description="With win man maintain car interesting cost night. Course option human scientist agent poor. Gun finally west around million firm.Gun drop though. Stay address lose.",
                             module_title="Module-2", estimated_duration=90),
        ]
        topics = [
            TopicDTOFactory(topic_id="T0001", module_id="M0001",
                            topic_type=TopicTypeEnum.LEARNING,
                            estimate_duration_in_mins=30),
            TopicDTOFactory(topic_id="T0002", module_id="M0002",
                            topic_type=TopicTypeEnum.LEARNING,
                            estimate_duration_in_mins=25),
        ]

        course_storage.check_course_exists.return_value = True
        module_storage.get_course_modules.return_value = modules
        topic_storage.get_topics_by_module_ids.return_value = topics

        # Act
        result = interactor.get_topics_for_course(course_id)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].topic_id == "T0001"
        assert result[1].topic_id == "T0002"

        # Snapshot
        snapshot.assert_match(
            json.dumps([r.__dict__ for r in result], sort_keys=True, indent=2,
                       cls=EnumEncoder),
            "topics_for_course_snapshot.json"
        )

    def test_course_not_found_raises(self, interactor, course_storage,
                                     module_storage,
                                     topic_storage, snapshot):
        # Arrange
        course_id = "C9999"
        course_storage.check_course_exists.return_value = False

        # Act
        with pytest.raises(CourseNotFound) as exc:
            interactor.get_topics_for_course(course_id)

        # Assert
        assert exc.value.course_id == "C9999"

        # snapshot
        snapshot.assert_match(
            json.dumps({"course_id": exc.value.course_id}, sort_keys=True,
                       indent=2),
            "course_not_found_snapshot.json"
        )
