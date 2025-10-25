from course_management.interactors.dtos import CreateTopicDTO, TopicDTO
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface,UserTopicCompletionPercentageDTO
from course_management.models import Topic
from typing import List


def get_existing_topic_ids(topic_ids : List[str]) -> List[str]:
    if not topic_ids:
        return []
    existing_ids = Topic.objects.filter(topic_id__in=topic_ids).values_list('topic_id',flat=True)
    return List(existing_ids)


class TopicStorage(TopicStorageInterface):

    def get_topic_types(self):
        pass

    def get_topics_with_module_ids(self, module_ids: list[str]):
        if not module_ids:
            return []

        topic_objects = Topic.objects.filter(module_id__in=module_ids)

        topic_dtos = []
        for t in topic_objects:
            topic_dto = TopicDTO(
                topic_id=t.topic_id,
                title=t.title,
                module_id=t.module_id,
                description=t.description,
                topic_type=t.topic_type,
                content=t.content,
                estimated_duration=t.estimated_duration
            )
            topic_dtos.append(topic_dto)

        return topic_dtos

    def get_topics_with_module_id(self,module_id : str)->list[TopicDTO]:
        pass

    def get_user_topic_progress(self, user_id: str, topic_id: str) -> UserTopicCompletionPercentageDTO:
        pass

    def get_user_topic_progresses(self, user_id: str, topic_id: str) -> list[UserTopicCompletionPercentageDTO]:
        pass

    def create_topics(self, topics: list[CreateTopicDTO]) -> List[TopicDTO]:
        topic_objects=[]
        for t in topics:
            topic=Topic.objects.create(
                title=t.title,
                description=t.description,
                module_id=t.module_id
            )
            topic_objects.append(topic)

        topic_dtos=[]
        for t in topic_objects:
            topic_dtos.append(
                TopicDTO(
                    topic_id=t.topic_id,
                    title=t.title,
                    description=t.description,
                    module_id=t.module_id
                )
            )
        return topic_dtos

    def update_topics(self,topics : list[TopicDTO])->list[TopicDTO]:
        topic_dtos= []
        for t in topics:
            topic_obj=Topic.objects.get(topic_id=t.topic_id)
            topic_obj.title=t.title
            topic_obj.description=t.description
            topic_obj.module_id=t.module_id
            topic_obj.save()

            topic_dtos.append(
                TopicDTO(
                    topic_id=topic_obj.topic_id,
                    title=topic_obj.title,
                    description=t.description,
                    module_id=t.module_id
                )
            )
        return topic_dtos

    def get_topics_for_topic_ids(self,topic_ids : list[str])->list[TopicDTO]:
        topic_objects=Topic.objects.filter(topic_id__in=topic_ids)
        topic_dtos=[]
        for t in topic_objects:
            topic_dtos.append(
                TopicDTO(
                    topic_id=t.topic_id,
                    title=t.title,
                    description=t.description,
                    module_id=t.module_id
                )
            )
        return topic_dtos

    def check_topic_exists(self,topic_id : str)->bool:
        return Topic.objects.filter(topic_id=topic_id).exists()


