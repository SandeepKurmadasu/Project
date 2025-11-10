from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import TopicDTO
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface


class GetTopicsForCourseInteractor(ValidationMixIn):

    def __init__(self, course_storage: CourseStorageInterface,
                 module_storage: ModuleStorageInterface,
                 topic_storage: TopicStorageInterface):
        self.course_storage = course_storage
        self.module_storage = module_storage
        self.topic_storage = topic_storage

    def get_topics_for_course(self, course_id: str) -> list[TopicDTO]:
        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)
        modules = self.module_storage.get_course_modules(course_id=course_id)
        module_ids = [obj.module_id for obj in modules]

        return self.topic_storage.get_topics_by_module_ids(
            module_ids=module_ids)
