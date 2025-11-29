from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface


class GetAssessmentByTopicInteractor(ValidationMixIn):

    def __init__(self, topic_storage: TopicStorageInterface,assessment_storage: AssessmentStorageInterface):
        self.topic_storage = topic_storage
        self.assessment_storage = assessment_storage


    def get_assessment_by_topic(self,topic_id: str):
        self.check_topic_exists(topic_id=topic_id,topic_storage=self.topic_storage)

        return self.assessment_storage.get_assessment_by_topic_id(topic_id=topic_id)