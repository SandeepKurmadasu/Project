"""Generate or update a course learning path based on current modules and topics."""

from collections import defaultdict

from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import (
    LearningPathForCourseDTO,
    LearningUnitDTO,
    CreateLearningUnitDTO,
)
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.learning_path_storage_interface import \
    LearningPathStorageInterface
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import \
    LearningUnitStorageInterface
from course_management.interactors.storage_interfaces.module_storage_interface import \
    ModuleStorageInterface
from course_management.interactors.storage_interfaces.topic_storage_interface import \
    TopicStorageInterface


class GenerateLearningPathForCourseInteractor(ValidationMixIn):
    """Interactor to create or update a course learning path."""

    def __init__(
            self,
            course_storage: CourseStorageInterface,
            module_storage: ModuleStorageInterface,
            topic_storage: TopicStorageInterface,
            learning_path_storage: LearningPathStorageInterface,
            learning_unit_storage: LearningUnitStorageInterface,
    ):
        self.course_storage = course_storage
        self.module_storage = module_storage
        self.topic_storage = topic_storage
        self.learning_path_storage = learning_path_storage
        self.learning_unit_storage = learning_unit_storage

    def generate_learning_path_for_course(self,
                                          course_id: str) -> LearningPathForCourseDTO:
        """
        Create or update the learning path for a course.

        If the current structure (modules/topics) matches the existing one,
        reuse the latest learning path. Otherwise, create a new version.
        """

        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)

        existing_path = self.learning_path_storage.get_latest_learning_path_by_course_id(
            course_id=course_id)

        if existing_path:
            existing_units = self.learning_unit_storage.get_learning_units_by_learning_path_id(
                existing_path.learning_path_id
            )
            is_same = self._is_learning_units_same(course_id, existing_units)

            if is_same:
                return existing_path

        new_learning_path = self._create_learning_path(course_id)
        self._add_learning_units(course_id, new_learning_path)

        return new_learning_path

    def _is_learning_units_same(self, course_id: str,
                                existing_units: list[LearningUnitDTO]) -> bool:
        """Check if the current course structure matches existing units."""
        ordered_modules = self._get_ordered_modules(course_id)
        topics_by_module = self._get_ordered_topics_by_module(ordered_modules)

        current_topic_ids = [
            topic.topic_id
            for module in ordered_modules
            for topic in topics_by_module.get(module.module_id, [])
        ]

        existing_topic_ids = [unit.topic_id for unit in existing_units]
        return current_topic_ids == existing_topic_ids

    def _create_learning_path(self,
                              course_id: str) -> LearningPathForCourseDTO:
        """Create a new course learning path entry."""

        return self.learning_path_storage.create_course_learning_path(
            course_id=course_id)

    def _add_learning_units(
            self, course_id: str, learning_path: LearningPathForCourseDTO
    ) -> list[LearningUnitDTO]:
        """Create learning units for all topics in the course."""
        ordered_modules = self._get_ordered_modules(course_id)
        topics_by_module = self._get_ordered_topics_by_module(ordered_modules)
        learning_units = self._build_learning_units(learning_path,
                                                    ordered_modules,
                                                    topics_by_module)

        return self.learning_unit_storage.create_learning_units(
            learning_units=learning_units)

    def _get_ordered_modules(self, course_id: str):
        """Fetch modules ordered by their order field."""
        modules = self.module_storage.get_course_modules(course_id=course_id)

        return sorted(modules, key=lambda m: m.order)

    def _get_ordered_topics_by_module(self, ordered_modules):
        """Fetch and group topics by module, ordered by their order field."""
        module_ids = [m.module_id for m in ordered_modules]
        topics = self.topic_storage.get_topics_by_module_ids(
            module_ids=module_ids)

        topics_by_module = defaultdict(list)
        for topic in topics:
            topics_by_module[topic.module_id].append(topic)

        for module_id in topics_by_module:
            topics_by_module[module_id].sort(key=lambda t: t.order)

        return topics_by_module

    @staticmethod
    def _build_learning_units(learning_path, ordered_modules,
                              topics_by_module):
        """Build learning unit DTOs in sequential order."""
        units = []
        order = 1
        for module in ordered_modules:
            for topic in topics_by_module.get(module.module_id, []):
                units.append(
                    CreateLearningUnitDTO(
                        learning_path_id=learning_path.learning_path_id,
                        unit_type=topic.topic_type,
                        topic_id=topic.topic_id,
                        unit_title=topic.title,
                        order=order,
                        estimated_duration_in_minutes=topic.estimate_duration_in_mins,
                    )
                )
                order += 1
        return units
