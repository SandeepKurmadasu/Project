import pytest
from unittest.mock import Mock, call
from faker import Faker
Faker.seed(42)
import json
from course_management.interactors.topics.topic_interactor import TopicInteractor
from course_management.exceptions.custom_exceptions import NotExistingTopicIdsFound, NotExistedTopicFound
from course_management.tests.factories import CreateTopicDTOFactory, TopicDTOFactory

@pytest.fixture
def reset_factories():
    CreateTopicDTOFactory.reset_sequence(0)
    TopicDTOFactory.reset_sequence(0)
    yield


@pytest.fixture
def topic_storage():
    s = Mock()
    s.create_topics.return_value = TopicDTOFactory.build()
    s.update_topics.return_value = []
    s.get_topics_for_topic_ids.return_value = []
    s.check_topic_exists.return_value = False  # topic doesn’t exist
    return s

@pytest.fixture
def user_storage():
    s = Mock()
    s.check_user_exists.return_value = True
    return s

@pytest.fixture
def interactor(topic_storage, user_storage):
    return TopicInteractor(topic_storage=topic_storage, user_storage=user_storage)


def test_create_topics_successfully(interactor, topic_storage,snapshot):
    CreateTopicDTOFactory.reset_sequence(0)
    TopicDTOFactory.reset_sequence(0)
    # Arrange
    topics = CreateTopicDTOFactory.build_batch(1)
    topic = TopicDTOFactory.build(topic_id="T0001")
    topic_storage.create_topics.return_value = topic

    # Act
    result = interactor.create_topics(topics)

    # Assert
    assert result.topic_id == "T0001"
    topic_storage.create_topics.assert_called_once_with(topics=topics)

    #snapshot
    snapshot.assert_match(
        result,
        "create_topics_snapshot.json"
    )


def test_update_topics_successfully(interactor, topic_storage,snapshot):
    # Arrange
    topics = [TopicDTOFactory.build(topic_id="T0001")]
    updated_topics = [TopicDTOFactory.build(topic_id="T0001", title="Updated Topic")]
    topic_storage.get_topics_for_topic_ids.return_value = topics
    topic_storage.update_topics.return_value = updated_topics

    # Act
    result = interactor.update_topics(topics)

    # Assert
    assert len(result) == 1
    assert result[0].topic_id == "T0001"
    assert result[0].title == "Updated Topic"
    topic_storage.update_topics.assert_called_once_with(topics=topics)

    #snapshot
    snapshot.assert_match(
         result,
        "update_topics_snapshot.json"
    )

def test_get_topics_successfully(interactor, topic_storage,snapshot):
    # Arrange
    topic_ids = ["T0001"]
    topics = [TopicDTOFactory.build(topic_id="T0001")]
    topic_storage.get_topics_for_topic_ids.return_value = topics

    # Act
    result = interactor.get_topics(topic_ids)

    # Assert
    assert len(result) == 1
    assert result[0].topic_id == "T0001"
    topic_storage.get_topics_for_topic_ids.assert_has_calls([call(topic_ids=topic_ids), call(topic_ids=topic_ids)])
    assert topic_storage.get_topics_for_topic_ids.call_count == 2

    #snapshot
    snapshot.assert_match(
         result,
        "get_topics_snapshot.json"
    )


def test_not_existing_topic_ids_update_raises(interactor, topic_storage,snapshot):
    # Arrange
    topics = [TopicDTOFactory.build(topic_id="T9999")]
    topic_storage.get_topics_for_topic_ids.return_value = []  # NO EXISTING TOPICS

    # Act
    with pytest.raises(NotExistingTopicIdsFound) as exc:
        interactor.update_topics(topics)

    # Assert
    assert exc.value.topic_ids == ["T9999"]

    #snapshot
    snapshot.assert_match(
        exc.value.topic_ids,
        "not_existing_topic_ids_update_snapshot.json"
    )

def test_not_existing_topic_ids_get_raises(interactor, topic_storage,snapshot):
    # Arrange
    topic_ids = ["T9999"]
    topic_storage.get_topics_for_topic_ids.return_value = []  # NO EXISTING TOPICS

    # Act
    with pytest.raises(NotExistingTopicIdsFound) as exc:
        interactor.get_topics(topic_ids)

    # Assert
    assert exc.value.topic_ids == ["T9999"]

    #snapshot
    snapshot.assert_match(
        exc.value.topic_ids,
        "not_existing_topic_ids_get_snapshot.json"
    )

def test_not_existed_topic_validate_raises(interactor, topic_storage,snapshot):
    # Arrange
    topic_id = "T9999"
    topic_storage.check_topic_exists.return_value = False

    # Act & Assert
    with pytest.raises(NotExistedTopicFound):
        interactor._validate_topic_id(topic_id)

    #snapshot
    snapshot.assert_match(
        topic_id,
        "not_existed_topic_validate_snapshot.json"
    )