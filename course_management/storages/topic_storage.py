from django.db.models import Sum

from course_management.interactors.dtos import CreateTopicDTO, \
    TopicDTO
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface
from course_management.models import Topic, Module, Course


class TopicStorage(TopicStorageInterface):

    def _update_module_and_course_duration(self, module_id, course_id):

        module_duration = Topic.objects.filter(
            module_id=module_id
        ).aggregate(
            total=Sum("estimated_duration_in_mins")
        )["total"] or 0

        Module.objects.filter(module_id=module_id).update(
            estimated_duration_in_min=module_duration
        )

        course_duration = Module.objects.filter(
            course_id=course_id
        ).aggregate(
            total=Sum("estimated_duration_in_min")
        )["total"] or 0

        Course.objects.filter(course_id=course_id).update(
            estimated_duration_in_min=course_duration
        )

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

        for t in created_topics:
            self._update_module_and_course_duration(
                module_id=t.module.module_id,
                course_id=t.module.course_id,
            )

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
            topic_id=str(each_topic.topic_id),
            module_id=str(each_topic.module.module_id),
            title=each_topic.topic_title,
            description=each_topic.description,
            topic_type=each_topic.topic_type,
            content=each_topic.content,
            order=each_topic.order,
            estimate_duration_in_mins=each_topic.estimated_duration_in_mins
        ) for each_topic in topics]

    def update_topics(self, topics: list[TopicDTO]) -> list[TopicDTO]:

        topic_ids = [t.topic_id for t in topics]
        db_topics = {str(t.topic_id): t for t in
                     Topic.objects.filter(topic_id__in=topic_ids)}

        updated_models = []

        for data in topics:
            model = db_topics[data.topic_id]

            model.topic_title = data.title
            model.description = data.description
            model.content = data.content
            model.estimated_duration_in_mins = data.estimate_duration_in_mins
            model.order = data.order
            model.topic_type = data.topic_type.value
            model.module_id = data.module_id

            updated_models.append(model)

        Topic.objects.bulk_update(
            updated_models,
            fields=[
                "topic_title",
                "description",
                "content",
                "estimated_duration_in_mins",
                "order",
                "topic_type",
                "module_id"
            ],
        )

        for data in topics:
            module = Module.objects.get(module_id=data.module_id)
            self._update_module_and_course_duration(
                module_id=data.module_id,
                course_id=module.course_id,
            )

        return topics


    def check_topic_exists(self, topic_id: str) -> bool:
        return Topic.objects.filter(topic_id=topic_id).exists()

    def get_topics_by_module_ids(self, module_ids: list[str]) -> list[
        TopicDTO]:
        topics = Topic.objects.filter(module_id__in=module_ids)

        return [TopicDTO(
            topic_id=str(each_topic.topic_id),
            module_id=str(each_topic.module.module_id),
            title=each_topic.topic_title,
            description=each_topic.description,
            topic_type=each_topic.topic_type,
            content=each_topic.content,
            order=each_topic.order,
            estimate_duration_in_mins=each_topic.estimated_duration_in_mins
        ) for each_topic in topics]
