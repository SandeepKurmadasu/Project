""" Handles creation of a new learning path for the user. """
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UserLearningPathDTO
from course_management.interactors.storage_interfaces.learning_path_storage_interface import \
    LearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from course_management.exceptions.custom_exceptions import \
    LearningPathIdNotFound


class StartUserCourseLearningPathInteractor(ValidationMixIn):
    """Start the user learning path interactor"""

    def __init__(self,
                 learning_path_storage: LearningPathStorageInterface,
                 user_storage: UserStorageInterface,
                 user_learning_storage: UserLearningPathStorageInterface):
        self.learning_path_storage = learning_path_storage
        self.user_storage = user_storage
        self.user_learning_storage = user_learning_storage

    def start_user_course_learning_path(self,
                                        user_id: str,
                                        course_learning_path_id: str) -> UserLearningPathDTO:
        """Main entry to start a user's course learning path"""

        self._validate_user_exists(user_id=user_id)
        self._validate_learning_path_exists(
            learning_path_id=course_learning_path_id
        )

        existing_user_path = self._get_existing_user_path(user_id,
                                                          course_learning_path_id)
        if existing_user_path:
            return existing_user_path

        return self._create_user_learning_path(user_id,
                                               course_learning_path_id)

    def _validate_user_exists(self, user_id: str):
        """Check if the user exists"""

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

    def _validate_learning_path_exists(self, learning_path_id: str):
        """Check if the learning path exists"""
        is_exists = self.learning_path_storage.learning_path_exist(
            learning_path_id=learning_path_id)

        if not is_exists:
            raise LearningPathIdNotFound(learning_path_id=learning_path_id)

    def _get_existing_user_path(self, user_id: str,
                                learning_path_id: str) -> UserLearningPathDTO | None:
        """Fetch an existing user learning path if any"""

        return self.user_learning_storage.get_user_learning_path_with_id(
            user_id=user_id,
            learning_path_id=learning_path_id
        )

    def _create_user_learning_path(self, user_id: str,
                                   learning_path_id: str) -> UserLearningPathDTO:
        """Create a new user learning path"""

        return self.user_learning_storage.create_user_learning_path(
            user_id=user_id,
            course_learning_path_id=learning_path_id)
