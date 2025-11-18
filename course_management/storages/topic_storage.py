from course_management.interactors.dtos import CreateTopicDTO, \
    TopicDTO
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.models import Topic, Module


class TopicStorage(TopicStorageInterface):

    def create_topics(self, topics: list[CreateTopicDTO]) -> list[TopicDTO]:

        topics_data = []

        module_ids = [t.module_id for t in topics]
        modules_map = {
            str(m.module_id): m
            for m in Module.objects.filter(module_id__in=module_ids)
        }

        for each_topic in topics:

            module = modules_map.get(each_topic.module_id)

            topic = Topic(
                module=module,
                topic_title=each_topic.title,
                description=each_topic.description,
                topic_type=each_topic.topic_type.value,
                content=each_topic.content,
                order=each_topic.order,
                estimated_duration_in_mins=each_topic.estimate_duration_in_mins,
            )

            topics_data.append(topic)

        created_topics = Topic.objects.bulk_create(topics_data)

        return [
            TopicDTO(
                topic_id=str(t.topic_id),
                module_id=str(t.module.module_id),
                title=t.topic_title,
                description=t.description,
                topic_type=t.topic_type,
                content=t.content,
                order=t.order,
                estimate_duration_in_mins=t.estimated_duration_in_mins,
            )
            for t in created_topics
        ]

    def get_topics_by_topic_ids(self, topic_ids: list[str]) -> list[TopicDTO]:
        topics = Topic.objects.filter(topic_id__in=topic_ids)
        return [TopicDTO(
            topic_id=each_topic.topic_id,
            module_id=each_topic.module.module_id,
            title=each_topic.topic_title,
            description=each_topic.description,
            topic_type=each_topic.topic_type,
            content=each_topic.content,
            order=each_topic.order,
            estimate_duration_in_mins=each_topic.estimated_duration_in_mins
        ) for each_topic in topics]

    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:
        topics_data = [
            Topic(
                topic_title=each_topic.title,
                description=each_topic.description,
                content=each_topic.content,
                estimated_duration_in_mins=each_topic.estimate_duration_in_mins
            ) for each_topic in topics
        ]
        Topic.objects.bulk_update(topics_data,
                                  fields=['topic_title', 'description',
                                          'content', 'estimated_duration_in_mins'])

        return [TopicDTO(
            topic_id=each_topic.topic_id,
            module_id=each_topic.module_id,
            title=each_topic.title,
            description=each_topic.description,
            topic_type=each_topic.topic_type,
            content=each_topic.content,
            order=each_topic.order,
            estimate_duration_in_mins=each_topic.estimate_duration_in_mins
        ) for each_topic in topics]

    def check_topic_exists(self, topic_id: str) -> bool:
        return Topic.objects.filter(topic_id=topic_id).exists()

    def get_topics_by_module_ids(self, module_ids: list[str]) -> list[
        TopicDTO]:
        topics = Topic.objects.filter(module_id__in=module_ids)

        return [TopicDTO(
            topic_id=each_topic.topic_id,
            module_id=each_topic.module.module_id,
            title=each_topic.topic_title,
            description=each_topic.description,
            topic_type=each_topic.topic_type,
            content=each_topic.content,
            order=each_topic.order,
            estimate_duration_in_mins=each_topic.estimated_duration_in_mins
        ) for each_topic in topics]
