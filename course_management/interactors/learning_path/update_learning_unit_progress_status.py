from course_management.exceptions.custom_exceptions import LearningUnitIdNotFound, \
    UserLearningUnitLockedException
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import AttemptedTopicStatusEnum, \
    UpdateLearningUnitProgressResponseDTO, UpdateLearningUnitProgressDTO
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface


class UpdateLearningUnitProgressStatusInteractor(ValidationMixIn):
    """Update the learning unit progress interactor"""

    def __init__(self, user_learning_storage: UserLearningPathStorageInterface,
                 user_learning_units_storage: UserLearningUnitStorageInterface):
        self.user_learning_storage = user_learning_storage
        self.user_learning_units_storage = user_learning_units_storage

    def update_learning_unit_progress_status(self, user_learning_path_id: str,
                                             user_learning_unit_id: int,
                                             status: AttemptedTopicStatusEnum,
                                             percentage: int) \
            -> UpdateLearningUnitProgressResponseDTO:
        """Update the user learning unit progress."""

        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_storage)

        self._validate_user_learning_unit_belongs_to_path(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_learning_unit_id)

        self._check_learning_unit_locked(
            user_learning_unit_id=user_learning_unit_id)

        updated_data = UpdateLearningUnitProgressDTO(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_learning_unit_id,
            status=status,
            percentage=percentage
        )

        self.user_learning_units_storage.update_learning_unit_progress(
            update_data=updated_data)

        next_unit_unlocked = False
        next_unit_id = None

        if status == AttemptedTopicStatusEnum.COMPLETE.value:

            next_unit = self._unlock_next_learning_unit(
                user_learning_path_id=user_learning_path_id,
                current_user_learning_unit_id=user_learning_unit_id
            )

            if next_unit:
                next_unit_unlocked = True
                next_unit_id = next_unit

        overall_percentage = self._calculate_overall_path_percentage(
            user_learning_path_id)

        self.user_learning_storage.update_user_learning_path_percentage(
            user_learning_path_id=user_learning_path_id,
            percentage=overall_percentage
        )

        return UpdateLearningUnitProgressResponseDTO(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_learning_unit_id,
            updated_status=status,
            updated_percentage=percentage,
            next_unit_unlocked=next_unit_unlocked,
            next_unit_id=next_unit_id,
            overall_path_percentage=overall_percentage
        )

    def _validate_user_learning_unit_belongs_to_path(self,
                                                     user_learning_path_id: str,
                                                     user_learning_unit_id: int):
        """Check user learning unit belongs to the user's learning path"""

        user_learning_unit = self.user_learning_units_storage.get_user_learning_unit_by_id(
            user_learning_unit_id=user_learning_unit_id)

        if not user_learning_unit:
            raise LearningUnitIdNotFound(
                learning_unit_id=str(user_learning_unit_id))

    def _unlock_next_learning_unit(self, user_learning_path_id: str,
                                   current_user_learning_unit_id: int):
        """Unlock the next user learning unit"""
        current_unit_progress = self.user_learning_units_storage.get_user_learning_unit_progress_by_id(
            user_learning_unit_id=current_user_learning_unit_id)

        next_unit = self.user_learning_units_storage.get_next_learning_unit(
            user_learning_path_id=user_learning_path_id,
            current_order=current_unit_progress.order)

        if not next_unit:
            return None

        self.user_learning_units_storage.unlock_learning_unit(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=next_unit.user_learning_unit_id
        )

        return next_unit.user_learning_unit_id

    def _calculate_overall_path_percentage(self,
                                           user_learning_path_id: str) -> int:
        """Calculate the learning path overall percentage"""

        all_units_progress = self.user_learning_units_storage.get_all_user_learning_unit_progress(
            user_learning_path_id=user_learning_path_id)

        if not all_units_progress:
            return 0

        total_percentage = sum(unit.percentage for unit in all_units_progress)
        overall_percentage = int(total_percentage / len(all_units_progress))

        return overall_percentage

    def _check_learning_unit_locked(self, user_learning_unit_id: int):
        """Check if the learning unit is locked"""
        unit_progress = self.user_learning_units_storage.get_user_learning_unit_progress_by_id(
            user_learning_unit_id=user_learning_unit_id
        )

        if unit_progress.is_locked:
            raise UserLearningUnitLockedException(
                user_learning_unit_id=user_learning_unit_id)
