from course_management.interactors.dtos import CreateTopicDTO, TopicDTO
from course_management.interactors.storage_interface.topic_storage_interface import TopicStorageInterface


class TopicStorage(TopicStorageInterface):

    def create_topics(self, topics: list[CreateTopicDTO]) -> TopicDTO:
        pass

    def get_topic_types(self):
        pass

    def get_topics_with_topic_ids(self,topic_ids : list[str])->list[TopicDTO]:
        pass

    def update_topics(self,topics : list[TopicDTO])->list[TopicDTO]:
        pass

    def check_topic_exists(self,topic_id : str)->bool:
        pass

    def get_topics_with_module_ids(self,module_ids : list[str])->list[TopicDTO]:
        pass

    def get_topics_with_module_id(self,module_id : str)->list[TopicDTO]:
        pass