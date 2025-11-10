from django.utils import timezone

from course_management.interactors.dtos import \
    UnitLearningProgressDTO, UserLearningUnitProgressDTO, \
    UpdateLearningUnitProgressDTO, LearningUnitDTO
from course_management.models import (
    UserLearningUnit, LearningUnit)

from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface


class UserLearningUnitStorage(UserLearningUnitStorageInterface):
    def get_all_user_learning_unit_progress(
            self, user_learning_path_id: str) -> list[UnitLearningProgressDTO]:

        user_units = (UserLearningUnit.objects.filter(
            user_learning_path_id=user_learning_path_id).
                      order_by("learning_unit__order"))

        return [UnitLearningProgressDTO(
            user_learning_path_id=unit.user_learning_path.user_learning_path_id,
            learning_unit_id=unit.learning_unit.learning_unit_id,
            status=unit.status,
            percentage=unit.percentage
        ) for unit in user_units]

    def get_user_learning_unit_progress(self, user_learning_path_id: str,
                                        learning_unit_id: str) -> UserLearningUnitProgressDTO:
        user_unit = UserLearningUnit.objects.select_related(
            "learning_unit").get(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id,
        )

        return UserLearningUnitProgressDTO(
            learning_unit_id=user_unit.learning_unit.learning_unit_id,
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            status=user_unit.status,
            percentage=user_unit.percentage,
            is_locked=user_unit.is_locked,
            order=user_unit.learning_unit.order,
            estimated_duration_in_minutes=user_unit.learning_unit.topic.estimated_duration_in_mins
        )

    def update_learning_unit_progress(self,
                                      update_data: UpdateLearningUnitProgressDTO
                                      ) -> UnitLearningProgressDTO:

        user_unit = UserLearningUnit.objects.get(
            user_learning_path_id=update_data.user_learning_path_id,
            learning_unit_id=update_data.learning_unit_id,
        )

        user_unit.progress_percentage = update_data.percentage
        user_unit.status = update_data.status

        if update_data.status == UserLearningUnit.AttemptStatusEnum.START:
            user_unit.started_at = timezone.now()
        elif update_data.status == UserLearningUnit.AttemptStatusEnum.COMPLETE:
            user_unit.completed_at = timezone.now()

        user_unit.save(update_fields=["percentage", "status", ])

        return UnitLearningProgressDTO(
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            learning_unit_id=user_unit.learning_unit.learning_unit_id,
            status=user_unit.status,
            percentage=user_unit.percentage
        )

    def get_next_learning_unit(self, user_learning_path_id: str,
                               current_order: int) -> LearningUnitDTO | None:
        next_unit = (LearningUnit.objects.filter(
            learning_path__user_learning_units__user_learning_path_id=user_learning_path_id,
            order__gt=current_order).order_by("order").first())

        if not next_unit:
            return None

        return LearningUnitDTO(
            learning_unit_id=next_unit.learning_unit_id,
            learning_path_id=next_unit.learning_path.learning_path_id,
            unit_type=next_unit.topic.topic_type,
            topic_id=next_unit.topic.topic_id,
            unit_title=next_unit.topic.topic_title,
            order=next_unit.order,
            estimated_duration_in_minutes=next_unit.topic.estimated_duration_in_mins
        )

    def unlock_learning_unit(self, user_learning_path_id: str,
                             learning_unit_id: str) -> UserLearningUnitProgressDTO:

        user_unit = UserLearningUnit.objects.get(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id)

        user_unit.is_locked = False
        user_unit.save(update_fields=["is_locked", "updated_at"])

        return UserLearningUnitProgressDTO(
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            learning_unit_id=user_unit.learning_unit.learning_unit_id,
            is_locked=user_unit.is_locked,
            status=user_unit.status,
            percentage=user_unit.percentage,
            order=user_unit.learning_unit.order,
            estimated_duration_in_minutes=user_unit.learning_unit.topic.estimated_duration_in_mins
        )

    def get_learning_units_by_topic_ids(self, user_id: str,
                                        topic_ids: list[str]
                                        ) -> list[UnitLearningProgressDTO]:

        user_units = UserLearningUnit.objects.filter(
            user_learning_path__user_id=user_id,
            learning_unit__topic_id__in=topic_ids)

        user_path_id = user_units[0].user_learning_path.user_learning_path_id
        return [UnitLearningProgressDTO(
            user_learning_path_id=user_path_id,
            learning_unit_id=unit.learning_unit.learning_unit_id,
            percentage=unit.percentage,
            status=unit.status
        ) for unit in user_units
        ]
