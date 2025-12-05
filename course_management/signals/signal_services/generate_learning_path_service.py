from course_management.interactors.learning_path.generate_learning_path_for_course import \
    GenerateLearningPathForCourseInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.learning_path_storage import \
    LearningPathStorage
from course_management.storages.learning_unit_storage import \
    LearningUnitStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage


class GenerateLearningPathService:

    @staticmethod
    def generate_learning_path_for_course(course_id: str):
        course_storage = CourseStorage()
        module_storage = ModuleStorage()
        topic_storage = TopicStorage()
        learning_path_storage = LearningPathStorage()
        learning_unit_storage = LearningUnitStorage()

        interactor = GenerateLearningPathForCourseInteractor(
            course_storage=course_storage,
            module_storage=module_storage, topic_storage=topic_storage,
            learning_path_storage=learning_path_storage,
            learning_unit_storage=learning_unit_storage
        )

        return interactor.generate_learning_path_for_course(course_id=course_id)