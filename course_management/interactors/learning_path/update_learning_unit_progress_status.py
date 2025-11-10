"""Create the interactor for the update learning unit progress interactor"""
from course_management.exceptions.custom_exceptions import \
    LearningUnitIdNotFound, LearningUnitLockedException
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UpdateLearningUnitProgressResponseDTO, \
    AttemptedTopicStatusEnum, UpdateLearningUnitProgressDTO
from course_management.interactors.storage_interfaces.learning_path_storage_interface import \
    LearningPathStorageInterface
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import \
    LearningUnitStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface


class UpdateLearningUnitProgressStatusInteractor(ValidationMixIn):
    """Update the learning unit progress interactor"""

    def __init__(self, learning_path_storage: LearningPathStorageInterface,
                 user_learning_storage: UserLearningPathStorageInterface,
                 learning_unit_storage: LearningUnitStorageInterface,
                 user_learning_units_storage: UserLearningUnitStorageInterface):
        self.learning_path_storage = learning_path_storage
        self.user_learning_storage = user_learning_storage
        self.learning_unit_storage = learning_unit_storage
        self.user_learning_units_storage = user_learning_units_storage

    def update_learning_unit_progress_status(self, user_learning_path_id: str,
                                             learning_unit_id: str,
                                             status: AttemptedTopicStatusEnum,
                                             percentage: int) \
            -> UpdateLearningUnitProgressResponseDTO:
        """Update the user learning unit progress."""

        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_storage)
        self._validate_learning_unit_belongs_to_path(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id)
        self._validate_learning_unit_exists(learning_unit_id)

        self._check_learning_unit_locked(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id)  # check once

        updated_data = UpdateLearningUnitProgressDTO(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id,
            status=status,
            percentage=percentage
        )
        self.user_learning_units_storage.update_learning_unit_progress(
            update_data=updated_data)

        next_unit_unlocked = False
        next_unit_id = None

        if status == AttemptedTopicStatusEnum.COMPLETE:
            next_unit_id = self._unlock_next_learning_unit(
                user_learning_path_id=user_learning_path_id,
                current_unit_id=learning_unit_id
            )
            next_unit_unlocked = next_unit_id is not None

        overall_percentage = self._calculate_overall_path_percentage(
            user_learning_path_id)

        self.user_learning_storage.update_user_learning_path_percentage(
            user_learning_path_id=user_learning_path_id,
            percentage=overall_percentage
        )

        return UpdateLearningUnitProgressResponseDTO(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id,
            updated_status=status,
            updated_percentage=percentage,
            next_unit_unlocked=next_unit_unlocked,
            next_unit_id=next_unit_id,
            overall_path_percentage=overall_percentage
        )

    def _validate_learning_unit_belongs_to_path(self,
                                                user_learning_path_id: str,
                                                learning_unit_id: str):
        """Check the learning unit belongs to the user's learning path"""

        all_units = self.learning_unit_storage.get_learning_units_by_learning_path_id(
            learning_path_id=user_learning_path_id)

        unit_ids = [unit.learning_unit_id for unit in all_units]

        if learning_unit_id not in unit_ids:
            raise LearningUnitIdNotFound(learning_unit_id=learning_unit_id)

    def _unlock_next_learning_unit(self, user_learning_path_id: str,
                                   current_unit_id: str):
        """Unlock the user next learning unit"""

        current_unit = self.learning_unit_storage.get_learning_unit(
            learning_unit_id=current_unit_id)

        next_unit = self.user_learning_units_storage.get_next_learning_unit(
            user_learning_path_id=user_learning_path_id,
            current_order=current_unit.order)

        if not next_unit:
            return None

        self.user_learning_units_storage.unlock_learning_unit(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=next_unit.learning_unit_id
        )

        return next_unit.learning_unit_id

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

    def _validate_learning_unit_exists(self, learning_unit_id: str):
        """Validate the learning unit"""

        exists = self.learning_unit_storage.check_learning_unit_exists(
            learning_unit_id=learning_unit_id)
        if not exists:
            raise LearningUnitIdNotFound(learning_unit_id=learning_unit_id)

    def _check_learning_unit_locked(self, user_learning_path_id: str,
                                    learning_unit_id: str):
        """Check the learning unit locked or not"""

        unit_progress = self.user_learning_units_storage.get_user_learning_unit_progress(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id
        )
        if unit_progress.is_locked:
            raise LearningUnitLockedException(
                learning_unit_id=learning_unit_id)
