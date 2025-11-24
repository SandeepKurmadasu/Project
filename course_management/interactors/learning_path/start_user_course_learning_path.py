""" Handles creation of a new learning path for the user. """
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import \
    UserLearningPathDTO, CreateUserLearningUnit
from course_management.interactors.learning_path.generate_learning_path_for_course import \
    GenerateLearningPathForCourseInteractor
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
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import \
    UserLearningUnitStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from course_management.exceptions.custom_exceptions import \
    LearningPathIdNotFound


class StartUserCourseLearningPathInteractor(ValidationMixIn):
    """Start the user learning path interactor"""

    def __init__(self,
                 learning_path_storage: LearningPathStorageInterface,
                 user_storage: UserStorageInterface,
                 user_learning_storage: UserLearningPathStorageInterface,
                 learning_unit_storage: LearningUnitStorageInterface,
                 user_learning_unit_storage: UserLearningUnitStorageInterface,
                 course_storage: CourseStorageInterface,
                 module_storage: ModuleStorageInterface,
                 topic_storage: TopicStorageInterface):
        self.learning_path_storage = learning_path_storage
        self.user_storage = user_storage
        self.user_learning_storage = user_learning_storage
        self.learning_unit_storage = learning_unit_storage
        self.user_learning_unit_storage = user_learning_unit_storage
        self.course_storage = course_storage
        self.topic_storage = topic_storage
        self.module_storage = module_storage

    def start_user_course_learning_path(self,
                                        user_id: str,
                                        course_id: str) -> UserLearningPathDTO:
        """Main entry to start a user's course learning path"""

        self._validate_user_exists(user_id=user_id)
        self.check_course_exists(course_id=course_id,
                                 course_storage=self.course_storage)

        learning_path = self.learning_path_storage.get_latest_learning_path_by_course_id(
            course_id=course_id)

        if not learning_path:
            generate_learning_path_interactor = GenerateLearningPathForCourseInteractor(
                course_storage=self.course_storage,
                learning_path_storage=self.learning_path_storage,
                learning_unit_storage=self.learning_unit_storage,
                module_storage=self.module_storage,
                topic_storage=self.topic_storage)

            learning_path = generate_learning_path_interactor.generate_learning_path_for_course(
                course_id=course_id)

        course_learning_path_id = learning_path.learning_path_id
        self._validate_learning_path_exists(
            learning_path_id=course_learning_path_id
        )

        existing_user_path = self._get_existing_user_path(user_id,
                                                          course_learning_path_id)

        if existing_user_path:
            return existing_user_path

        get_learning_path_units = self.learning_unit_storage.get_learning_units_by_learning_path_id(
            learning_path_id=course_learning_path_id)
        learning_unit_ids = [obj.learning_unit_id for obj in
                             get_learning_path_units]

        user_learning_path = self._create_user_learning_path(user_id=user_id,
                                                             learning_path_id=course_learning_path_id)

        create_learning_unit_input = [CreateUserLearningUnit(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            learning_unit_id=each_unit_id
        ) for each_unit_id in learning_unit_ids]

        self.user_learning_unit_storage.create_user_learning_units(
            create_learning_unit_input)

        return user_learning_path

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

        user_learning_path = self.user_learning_storage.get_user_learning_path_with_id(
            user_id=user_id,
            learning_path_id=learning_path_id
        )
        return user_learning_path

    def _create_user_learning_path(self, user_id: str,
                                   learning_path_id: str) -> UserLearningPathDTO:
        """Create a new user learning path"""

        return self.user_learning_storage.create_user_learning_path(
            user_id=user_id,
            course_learning_path_id=learning_path_id)
