"""Get user learning path interactor"""
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UserLearningPathDTO, UserLearningPathPercentageDTO, LearningUnitProgressDTO
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    (UserLearningUnitStorageInterface)


class GetUserLearningPathDetailsInteractor(ValidationMixIn):
    """ Get the user learning details """
    def __init__(self,
                 user_learning_path_storage: UserLearningPathStorageInterface,
                 user_learning_unit_storage: UserLearningUnitStorageInterface):
        self.user_learning_path_storage = user_learning_path_storage
        self.user_learning_unit_storage = user_learning_unit_storage

    def get_user_learning_path(self,
                               user_learning_path_id: str) -> UserLearningPathDTO:
        """ Get the learning path for user"""
        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_path_storage)

        return self.user_learning_path_storage.get_user_learning_path_with_user_learning_path_id(
            user_learning_path_id=user_learning_path_id)

    def get_user_learning_path_percentage(self,
                                          user_learning_path_id: str) \
            -> UserLearningPathPercentageDTO:
        """get the user learning path percentage """

        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_path_storage)

        user_learning_data = (
            self.user_learning_path_storage.get_user_learning_path_with_user_learning_path_id(
                user_learning_path_id=user_learning_path_id))

        return UserLearningPathPercentageDTO(
            user_id=user_learning_data.user_id,
            learning_path_id=user_learning_data.learning_path_id,
            percentage=user_learning_data.overall_percentage
        )

    def get_current_learning_unit_status(self,
                                         user_learning_path_id: str) -> LearningUnitProgressDTO:
        """ Get the user current learning unit status"""
        self.validate_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id,
            user_learning_path_storage=self.user_learning_path_storage)
        user_learning_path = (
            self.user_learning_path_storage.get_user_learning_path_with_user_learning_path_id(
                user_learning_path_id=user_learning_path_id))
        current_learning_unit_id = user_learning_path.current_learning_unit_id

        current_unit_progress = self.user_learning_unit_storage.get_user_learning_unit_progress(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=current_learning_unit_id)

        return LearningUnitProgressDTO(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=current_learning_unit_id,
            status=current_unit_progress.status,
            percentage=current_unit_progress.percentage
        )
