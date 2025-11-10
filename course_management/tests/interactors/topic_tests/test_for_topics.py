import pytest
from unittest.mock import Mock
from course_management.interactors.dtos import (
    UserTopicCompletionPercentageDTO, TopicTypeEnum
    )
from course_management.exceptions.custom_exceptions import (
    NotExistingTopicTypesFound, NotExistingTopicIdsFound, NotExistedTopicFound,
    UserNotFound
)
from course_management.interactors.topic.topic_interactor import \
    TopicsInteractor
from course_management.tests.factories.interactor_factories import \
    CreateTopicDTOFactory, \
    TopicDTOFactory


@pytest.fixture
def topic_storage():
    s = Mock()
    return s


@pytest.fixture
def user_storage():
    s = Mock()
    return s


@pytest.fixture
def user_learning_unit_storage():
    s = Mock()
    return s


@pytest.fixture
def interactor(topic_storage, user_storage, user_learning_unit_storage):
    return TopicsInteractor(
        topic_storage=topic_storage,
        user_storage=user_storage,
        user_learning_unit_storage=user_learning_unit_storage,
    )


class TestTopicInteractor:
    def test_create_topics_success(self, interactor, topic_storage):
        topics = [
            CreateTopicDTOFactory(title="T1", topic_type=TopicTypeEnum.ASSESSMENT),
            CreateTopicDTOFactory(title="T2", topic_type=TopicTypeEnum.LEARNING),
        ]

        topic_storage.create_topics.return_value = [
            TopicDTOFactory(topic_id="T001", title="T1",
                            topic_type=TopicTypeEnum.ASSESSMENT),
            TopicDTOFactory(topic_id="T002", title="T2",
                            topic_type=TopicTypeEnum.LEARNING),
        ]

        result = interactor.create_topics(topics)

        assert len(result) == 2
        topic_storage.create_topics.assert_called_once_with(topics=topics)

    def test_create_topics_with_invalid_type_raises(self, interactor):
        class FakeTopicType:
            value = "INVALID_TYPE"

        topics = [
            CreateTopicDTOFactory(title="BadTypeTopic", topic_type=FakeTopicType())
        ]

        with pytest.raises(NotExistingTopicTypesFound):
            interactor.create_topics(topics=topics)

    def test_update_topics_success(self, interactor, topic_storage):
        topic_storage.get_topics_by_topic_ids.return_value = [
            TopicDTOFactory(topic_id="T001", title="Old",
                            topic_type=TopicTypeEnum.ASSESSMENT)
        ]

        topics = [
            TopicDTOFactory(topic_id="T001", title="Updated",
                            topic_type=TopicTypeEnum.ASSESSMENT)
        ]

        topic_storage.update_topics.return_value = topics

        result = interactor.update_topics(topics)

        assert result == topics
        topic_storage.update_topics.assert_called_once()

    def test_update_topics_with_nonexistent_topic_id(self, interactor, topic_storage):
        topic_storage.get_topics_by_topic_ids.return_value = []

        topics = [
            TopicDTOFactory(topic_id="T999", title="Missing",
                            topic_type=TopicTypeEnum.ASSESSMENT)
        ]

        with pytest.raises(NotExistingTopicIdsFound):
            interactor.update_topics(topics)

    def test_get_topics_success(self, interactor, topic_storage):
        topic_storage.get_topics_by_topic_ids.return_value = [
            TopicDTOFactory(topic_id="T001", title="Networking",
                            topic_type=TopicTypeEnum.LEARNING)
        ]

        result = interactor.get_topics(["T001"])
        assert result[0].topic_id == "T001"

    def test_get_topics_invalid_id_raises(self, interactor, topic_storage):
        topic_storage.get_topics_by_topic_ids.return_value = []

        with pytest.raises(NotExistingTopicIdsFound):
            interactor.get_topics(["T404"])

    def test_user_topic_completion_percentage_success(self, interactor, user_storage,
                                                      topic_storage,
                                                      user_learning_unit_storage):
        user_storage.get_user_ids_in_db.return_value = ["U001"]
        topic_storage.check_topic_exists.return_value = True
        user_learning_unit_storage.get_learning_units_by_topic_ids.return_value = [
            Mock(percentage=80)
        ]

        result = interactor.get_user_topic_completion_percentage(user_id="U001",
                                                                 topic_id="T001")

        assert isinstance(result, UserTopicCompletionPercentageDTO)
        assert result.percentage == 80

    def test_user_not_found_raises(self, interactor, user_storage, topic_storage):
        user_storage.check_user_exists.return_value = False
        topic_storage.check_topic_exists.return_value = True
        interactor.user_learning_unit_storage.get_learning_units_by_topic_ids.return_value = []

        with pytest.raises(UserNotFound):
            interactor.get_user_topic_completion_percentage(user_id="U999",
                                                            topic_id="T001")

    def test_topic_not_found_raises(self, interactor, user_storage, topic_storage):
        user_storage.get_user_ids_in_db.return_value = ["U001"]
        topic_storage.check_topic_exists.return_value = False

        with pytest.raises(NotExistedTopicFound):
            interactor.get_user_topic_completion_percentage(user_id="U001",
                                                            topic_id="T999")

    def test_no_learning_units_returns_zero(self, interactor, user_storage, topic_storage,
                                            user_learning_unit_storage):
        user_storage.get_user_ids_in_db.return_value = ["U001"]
        topic_storage.check_topic_exists.return_value = True
        user_learning_unit_storage.get_learning_units_by_topic_ids.return_value = []

        result = interactor.get_user_topic_completion_percentage(user_id="U001",
                                                                 topic_id="T001")

        assert result.percentage == 0
