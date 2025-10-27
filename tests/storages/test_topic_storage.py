import pytest
from course_management.storages.topic_storage import TopicStorage, get_existing_topic_ids
from course_management.models import Topic, Module, Course
from course_management.interactors.dtos import CreateTopicDTO, TopicDTO


@pytest.mark.django_db
def test_get_existing_topic_ids():
    # ARRANGE
    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )
    topic1 = Topic.objects.create(
        title='Topic 1',
        description='First topic',
        module=module,
        topic_type='VIDEO',
        content='Content',
        estimated_duration=30
    )
    topic2 = Topic.objects.create(
        title='Topic 2',
        description='Second topic',
        module=module,
        topic_type='ARTICLE',
        content='Content',
        estimated_duration=15
    )

    # ACT
    result = get_existing_topic_ids([str(topic1.topic_id), str(topic2.topic_id), 'invalid_id'])

    # ASSERT
    assert len(result) == 2
    assert str(topic1.topic_id) in result
    assert str(topic2.topic_id) in result


@pytest.mark.django_db
def test_get_topics_with_module_ids():
    # ARRANGE
    storage = TopicStorage()

    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module1 = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )
    module2 = Module.objects.create(
        module_title='Module 2',
        description='Advanced',
        course=course
    )

    _topic1 = Topic.objects.create(
        title='Topic 1',
        description='First topic',
        module=module1,
        topic_type='VIDEO',
        content='Content',
        estimated_duration=30
    )
    _topic2 = Topic.objects.create(
        title='Topic 2',
        description='Second topic',
        module=module2,
        topic_type='ARTICLE',
        content='Content',
        estimated_duration=15
    )

    # ACT
    result = storage.get_topics_with_module_ids([str(module1.module_id), str(module2.module_id)])

    # ASSERT
    assert len(result) == 2
    result_module_ids = [r.module_id for r in result]
    assert str(module1.module_id) in result_module_ids
    assert str(module2.module_id) in result_module_ids

@pytest.mark.django_db
def test_create_topics():
    # ARRANGE
    storage = TopicStorage()

    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )

    topics_to_create = [
        CreateTopicDTO(
            title='Topic 1',
            description='First topic',
            module_id=str(module.module_id),
            topic_type='VIDEO',
            content='Video content',
            estimate_duration=30
        ),
        CreateTopicDTO(
            title='Topic 2',
            description='Second topic',
            module_id=str(module.module_id),
            topic_type='ARTICLE',
            content='Article content',
            estimate_duration=15
        )
    ]

    # ACT
    result = storage.create_topics(topics_to_create)

    # ASSERT
    assert len(result) == 2
    assert result[0].title == 'Topic 1'
    assert result[1].title == 'Topic 2'
    assert Topic.objects.count() == 2


@pytest.mark.django_db
def test_update_topics():
    # ARRANGE
    storage = TopicStorage()

    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )
    topic = Topic.objects.create(
        title='Original Title',
        description='Original Description',
        module=module,
        topic_type='VIDEO',
        content='Content',
        estimated_duration=30
    )

    updated_topics = [
        TopicDTO(
            topic_id=str(topic.topic_id),
            title='Updated Title',
            description='Updated Description',
            module_id=str(module.module_id),
            topic_type='VIDEO',
            content='Content',
            estimated_duration=30
        )
    ]

    # ACT
    result = storage.update_topics(updated_topics)

    # ASSERT
    assert len(result) == 1
    assert result[0].title == 'Updated Title'
    topic.refresh_from_db()
    assert topic.title == 'Updated Title'


@pytest.mark.django_db
def test_get_topics_for_topic_ids():
    # ARRANGE
    storage = TopicStorage()

    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )
    topic1 = Topic.objects.create(
        title='Topic 1',
        description='First topic',
        module=module,
        topic_type='VIDEO',
        content='Content',
        estimated_duration=30
    )
    topic2 = Topic.objects.create(
        title='Topic 2',
        description='Second topic',
        module=module,
        topic_type='ARTICLE',
        content='Content',
        estimated_duration=15
    )

    # ACT
    result = storage.get_topics_for_topic_ids([str(topic1.topic_id), str(topic2.topic_id)])

    # ASSERT
    assert len(result) == 2
    result_ids = [r.topic_id for r in result]
    assert str(topic1.topic_id) in result_ids
    assert str(topic2.topic_id) in result_ids


@pytest.mark.django_db
def test_check_topic_exists():
    # ARRANGE
    storage = TopicStorage()

    course = Course.objects.create(
        title='Python Course',
        description='Learn Python',
        category='Programming',
        level='BEGINNER'
    )
    module = Module.objects.create(
        module_title='Module 1',
        description='Introduction',
        course=course
    )
    topic = Topic.objects.create(
        title='Topic 1',
        description='First topic',
        module=module,
        topic_type='VIDEO',
        content='Content',
        estimated_duration=30
    )

    # ACT & ASSERT
    assert storage.check_topic_exists(str(topic.topic_id)) is True
    assert storage.check_topic_exists('invalid_topic_id') is False