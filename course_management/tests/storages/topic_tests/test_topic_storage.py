import json
import pytest
import uuid

from course_management.interactors.dtos import (
    CreateTopicDTO,
    TopicDTO,
    TopicTypeEnum,
)
from course_management.models import Topic, Module
from course_management.storages.topic_storage import TopicStorage

TID1 = uuid.UUID("11111111-1111-1111-1111-111111111111")
TID2 = uuid.UUID("22222222-2222-2222-2222-222222222222")
MID1 = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


class TestTopics:
    @pytest.mark.django_db
    def test_create_topics(self, snapshot):
        Module.objects.create(
            module_id=MID1,
            module_title="Module 1",
            description="D1",
            order=1,
            estimated_duration_in_min=60,
        )

        dto = CreateTopicDTO(
            module_id=MID1,
            title="Topic A",
            description="Desc A",
            order=1,
            topic_type=TopicTypeEnum.LEARNING,
            content="Content A",
            estimate_duration_in_mins=30,
        )

        storage = TopicStorage()
        result = storage.create_topics([dto])
        output = [f"{each.title} - {each.module_id}" for each in result]

        snapshot.assert_match(repr(output), "Test_create_topics.txt")

    @pytest.mark.django_db
    def test_get_topics_by_topic_ids(self, snapshot):
        module = Module.objects.create(
            module_id=MID1,
            module_title="Module 1",
            description="D1",
            order=1,
            estimated_duration_in_min=60,
        )

        Topic.objects.create(
            topic_id=TID1,
            module=module,
            topic_title="Topic A",
            description="Desc A",
            topic_type="LEARNING",
            content="Content A",
            order=1,
            estimated_duration_in_mins=20,
        )

        storage = TopicStorage()
        result = storage.get_topics_by_topic_ids([str(TID1)])

        snapshot.assert_match(repr(result), "Test_get_topics_by_topic_ids.txt")

    @pytest.mark.django_db
    def test_update_topics(self, snapshot):
        module = Module.objects.create(
            module_id=MID1,
            module_title="Module 1",
            description="D1",
            order=1,
            estimated_duration_in_min=60,
        )

        Topic.objects.create(
            topic_id=TID2,
            module=module,
            topic_title="Old Title",
            description="Old Desc",
            topic_type="LEARNING",
            content="Old Content",
            order=2,
            estimated_duration_in_mins=15,
        )

        dto = TopicDTO(
            topic_id=str(TID2),
            module_id=str(MID1),
            title="New Title",
            description="New Desc",
            topic_type=TopicTypeEnum.LEARNING,
            content="New Content",
            order=2,
            estimate_duration_in_mins=40,
        )

        storage = TopicStorage()
        result = storage.update_topics([dto])

        snapshot.assert_match(repr(result), "test_update_topics.txt")

    @pytest.mark.django_db
    def test_check_topic_exists(self, snapshot):
        module = Module.objects.create(
            module_id=MID1,
            module_title="Module X",
            description="DX",
            order=1,
            estimated_duration_in_min=50,
        )

        Topic.objects.create(
            topic_id=TID1,
            module=module,
            topic_title="Exists",
            description="Something",
            topic_type="LEARNING",
            content="C",
            order=1,
            estimated_duration_in_mins=10,
        )

        storage = TopicStorage()
        result = storage.check_topic_exists(str(TID1))

        snapshot.assert_match(
            json.dumps(result, sort_keys=True, indent=2),
            "check_topic_exists.json",
        )

    @pytest.mark.django_db
    def test_get_topics_by_module_ids(self, snapshot):
        module = Module.objects.create(
            module_id=MID1,
            module_title="Module 1",
            description="D1",
            order=1,
            estimated_duration_in_min=60,
        )

        Topic.objects.create(
            topic_id=TID1,
            module=module,
            topic_title="Topic A",
            description="Desc A",
            topic_type="LEARNING",
            content="C A",
            order=1,
            estimated_duration_in_mins=25,
        )

        storage = TopicStorage()
        result = storage.get_topics_by_module_ids([str(MID1)])

        snapshot.assert_match(repr(result), "get_topics_by_module_ids.json")
