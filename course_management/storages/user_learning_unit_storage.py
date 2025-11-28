from course_management.interactors.dtos import \
    LearningUnitProgressDTO, UserLearningUnitProgressDTO, \
    UpdateLearningUnitProgressDTO, LearningUnitDTO, UserLearningUnitDTO, \
    CreateUserLearningUnit, UserLearningUnitTopicsProgressDTO
from course_management.models import (
    UserLearningUnit, LearningUnit, UserLearningPath)

from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface


class UserLearningUnitStorage(UserLearningUnitStorageInterface):

    def create_user_learning_units(self, user_learning_units: list[
        CreateUserLearningUnit]) -> list[UserLearningUnitDTO]:

        user_learning_path = UserLearningPath.objects.get(
            user_learning_path_id=user_learning_units[0].user_learning_path_id)
        unit_ids = {dto.learning_unit_id for dto in user_learning_units}
        units = {str(unit.learning_unit_id): unit
                 for unit in LearningUnit.objects.filter(pk__in=unit_ids)}

        model_objects = []
        for dto in user_learning_units:
            model_objects.append(
                UserLearningUnit(
                    user_learning_path=user_learning_path,
                    learning_unit=units[str(dto.learning_unit_id)]))

        created_units = UserLearningUnit.objects.bulk_create(model_objects)

        first_unit = (UserLearningUnit.objects
                      .filter(user_learning_path=user_learning_path)
                      .order_by("learning_unit__order").first())
        first_unit.is_locked = False
        first_unit.save(update_fields=["is_locked"])

        units = UserLearningUnit.objects.filter(
            pk__in=[u.pk for u in created_units])

        return [UserLearningUnitDTO(
            user_learning_path_id=unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=unit.pk,
            is_locked=unit.is_locked,
            percentage=unit.percentage,
            status=unit.status,
        ) for unit in units]

    def get_all_user_learning_unit_progress(self, user_learning_path_id: str) \
            -> list[LearningUnitProgressDTO]:

        user_units = (UserLearningUnit.objects.filter(
            user_learning_path_id=user_learning_path_id).
                      order_by("learning_unit__order"))

        return [LearningUnitProgressDTO(
            user_learning_path_id=unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=unit.pk,
            status=unit.status,
            percentage=unit.percentage
        ) for unit in user_units]

    def get_user_learning_unit_progress(self, user_learning_path_id: str,
                                        learning_unit_id: str) -> UserLearningUnitProgressDTO:
        user_unit = UserLearningUnit.objects.get(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id,
        )

        return UserLearningUnitProgressDTO(
            user_learning_unit_id=user_unit.pk,
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            status=user_unit.status,
            percentage=user_unit.percentage,
            is_locked=user_unit.is_locked,
            order=user_unit.learning_unit.order,
            estimated_duration_in_minutes=user_unit.learning_unit.topic.estimated_duration_in_mins
        )

    def update_learning_unit_progress(self,
                                      update_data: UpdateLearningUnitProgressDTO
                                      ) -> LearningUnitProgressDTO:

        user_unit = UserLearningUnit.objects.get(
            user_learning_path_id=update_data.user_learning_path_id,
            id=update_data.user_learning_unit_id,
        )

        user_unit.percentage = update_data.percentage
        user_unit.status = update_data.status

        user_unit.save(update_fields=["percentage", "status", ])

        return LearningUnitProgressDTO(
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=user_unit.pk,
            status=user_unit.status,
            percentage=user_unit.percentage
        )

    def get_next_learning_unit(self, user_learning_path_id: str,
                               current_order: int) -> UserLearningUnitDTO | None:
        next_unit = (UserLearningUnit.objects.filter(
            user_learning_path_id=user_learning_path_id,
            learning_unit__order__gt=current_order).order_by(
            "learning_unit__order").first())

        return UserLearningUnitDTO(
            user_learning_unit_id=next_unit.pk,
            user_learning_path_id=user_learning_path_id,
            is_locked=next_unit.is_locked,
            status=next_unit.status,
            percentage=next_unit.percentage
        )

    def unlock_learning_unit(self, user_learning_path_id: str,
                             user_learning_unit_id: int) -> UserLearningUnitProgressDTO:

        user_unit = UserLearningUnit.objects.get(
            user_learning_path_id=user_learning_path_id,
            id=user_learning_unit_id)

        user_unit.is_locked = False
        user_unit.save(update_fields=["is_locked", "updated_at"])

        return UserLearningUnitProgressDTO(
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=user_unit.pk,
            is_locked=user_unit.is_locked,
            status=user_unit.status,
            percentage=user_unit.percentage,
            order=user_unit.learning_unit.order,
            estimated_duration_in_minutes=user_unit.learning_unit.topic.estimated_duration_in_mins
        )

    def get_learning_units_by_topic_ids(self, user_id: str,
                                        topic_ids: list[str]
                                        ) -> list[LearningUnitProgressDTO]:

        user_units = UserLearningUnit.objects.filter(
            user_learning_path__user_id=user_id,
            learning_unit__topic_id__in=topic_ids)

        return [LearningUnitProgressDTO(
            user_learning_path_id=unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=unit.pk,
            percentage=unit.percentage,
            status=unit.status
        ) for unit in user_units]

    def get_user_learning_unit_by_id(self,
                                     user_learning_unit_id: int) -> UserLearningUnitDTO:

        user_learning_unit_data = UserLearningUnit.objects.get(
            id=user_learning_unit_id)

        return UserLearningUnitDTO(
            user_learning_path_id=user_learning_unit_data.user_learning_path.user_learning_path_id,
            user_learning_unit_id=user_learning_unit_id,
            is_locked=user_learning_unit_data.is_locked,
            status=user_learning_unit_data.status,
            percentage=user_learning_unit_data.percentage
        )

    def get_user_learning_unit_progress_by_id(self,
                                              user_learning_unit_id: int) -> UserLearningUnitProgressDTO | None:
        user_unit = UserLearningUnit.objects.get(id=user_learning_unit_id)

        if not user_unit:
            return None

        return UserLearningUnitProgressDTO(
            user_learning_path_id=user_unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=user_unit.pk,
            is_locked=user_unit.is_locked,
            status=user_unit.status,
            percentage=user_unit.percentage,
            order=user_unit.learning_unit.order,
            estimated_duration_in_minutes=user_unit.learning_unit.topic.estimated_duration_in_mins
        )


    def get_user_learning_units_progress(self, user_learning_path_id: str)-> list[UserLearningUnitTopicsProgressDTO]:

        user_units = (UserLearningUnit.objects.filter(
            user_learning_path_id=user_learning_path_id).
                      order_by("learning_unit__order"))

        return [UserLearningUnitTopicsProgressDTO(
            user_learning_path_id=unit.user_learning_path.user_learning_path_id,
            user_learning_unit_id=unit.pk,
            topic_id=unit.learning_unit.topic.topic_id,
            module_id=unit.learning_unit.topic.module.module_id,
            status=unit.status,
            is_locked=unit.is_locked,
            percentage=unit.percentage
        ) for unit in user_units]


