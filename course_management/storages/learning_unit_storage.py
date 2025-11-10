from course_management.interactors.dtos import (
    LearningUnitDTO,
    CreateLearningUnitDTO,
)
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import (
    LearningUnitStorageInterface,
)
from course_management.models import LearningUnit, \
    CourseLearningPath, Topic


class LearningUnitStorage(LearningUnitStorageInterface):
    def check_learning_unit_exists(self, learning_unit_id: str) -> bool:
        """
        Checks if a learning unit exists by ID.
        """
        return LearningUnit.objects.filter(
            learning_unit_id=learning_unit_id).exists()

    def get_learning_unit(self, learning_unit_id: str) -> LearningUnitDTO:
        """
        Fetch a learning unit by ID and convert to DTO.
        """
        unit = LearningUnit.objects.select_related("learning_path",
                                                   "topic").get(
            learning_unit_id=learning_unit_id
        )

        return LearningUnitDTO(
            learning_unit_id=str(unit.learning_unit_id),
            learning_path_id=str(unit.learning_path.learning_path_id),
            unit_title=unit.topic.topic_title,
            order=unit.order,
            topic_id=str(unit.topic.topic_id) if unit.topic else None,
            unit_type=unit.topic.topic_type,
            estimated_duration_in_minutes=unit.topic.estimated_duration_in_minutes,
        )

    def create_learning_units(
            self, learning_units: list[CreateLearningUnitDTO]
    ) -> list[LearningUnitDTO]:
        """
        Bulk creates learning units from a list of CreateLearningUnitDTOs.
        """
        if not learning_units:
            return []

        learning_path = CourseLearningPath.objects.get(
            learning_path_id=learning_units[0].learning_path_id
        )

        units_to_create = []
        for each_unit in learning_units:
            topic = Topic.objects.get(topic_id=each_unit.topic_id)

            units_to_create.append(
                LearningUnit(
                    learning_path=learning_path,
                    topic=topic,
                    unit_title=each_unit.unit_title,
                    order=each_unit.order,
                    unit_type=each_unit.unit_type,
                    estimated_duration_in_minutes=each_unit.estimated_duration_in_minutes,
                )
            )

        created_units = LearningUnit.objects.bulk_create(units_to_create)

        # Convert to DTOs
        return [
            LearningUnitDTO(
                learning_unit_id=str(unit.learning_unit_id),
                learning_path_id=str(unit.learning_path.learning_path_id),
                unit_title=unit.topic.topic_title,
                order=unit.order,
                topic_id=str(unit.topic.topic_id),
                unit_type=unit.topic.topic_type,
                estimated_duration_in_minutes=unit.topic.estimated_duration_in_minutes,
            ) for unit in created_units
        ]

    def get_learning_units_by_learning_path_id(
            self, learning_path_id: str
    ) -> list[LearningUnitDTO]:
        """
        Returns all learning units for a given learning_path_id ordered by 'order'.
        """
        units = (
            LearningUnit.objects.select_related("topic", "learning_path")
            .filter(learning_path_id=learning_path_id)
            .order_by("order")
        )

        return [
            LearningUnitDTO(
                learning_unit_id=str(unit.learning_unit_id),
                learning_path_id=str(unit.learning_path.learning_path_id),
                unit_title=unit.topic.topic_title,
                order=unit.order,
                topic_id=str(unit.topic.topic_id),
                unit_type=unit.topic.topic_type,
                estimated_duration_in_minutes=unit.topic.estimated_duration_in_minutes,
            ) for unit in units
        ]
