import pytest
from unittest.mock import Mock
from course_management.interactors.modules.get_user_module_completion_percentage import (
    GetUserModuleCompletionPercentageInteractor,
)
from course_management.interactors.dtos import \
    UserModuleCompletionPercentageDTO
from course_management.exceptions.custom_exceptions import (
    UserNotEnrolledInModule,
    LearningPathNotFound, UserNotFound, DBNotFoundedModuleIds,
)


@pytest.fixture
def user_storage():
    mock_storage = Mock()
    mock_storage.get_user_ids_in_db.return_value = ["U001"]
    return mock_storage


@pytest.fixture
def module_storage():
    s = Mock()

    s.get_db_existing_module_ids.return_value = ["M001", "M002", "M003"]

    s.get_modules.return_value = [
        Mock(course_id="C001", module_id="M001"),
        Mock(course_id="C002", module_id="M002"),
    ]

    # ✅ If other tests use this
    s.get_modules_for_courses.return_value = [
        Mock(module_id="M001"),
        Mock(module_id="M002"),
    ]

    return s


@pytest.fixture
def topic_storage():
    mock_storage = Mock()
    mock_storage.get_topics_by_module_ids.return_value = [
        Mock(topic_id="T001"), Mock(topic_id="T002")
    ]
    return mock_storage


@pytest.fixture
def enrollment_storage():
    mock_storage = Mock()
    mock_storage.check_user_course_enrollment_exist.return_value = True
    return mock_storage


@pytest.fixture
def user_learning_path_storage():
    mock_storage = Mock()
    mock_storage.get_user_learning_path.return_value = Mock()
    return mock_storage


@pytest.fixture
def user_learning_unit_storage():
    mock_storage = Mock()
    mock_storage.get_learning_units_by_topic_ids.return_value = [
        Mock(percentage=60),
        Mock(percentage=80),
    ]
    return mock_storage


@pytest.fixture
def interactor(
        user_storage,
        module_storage,
        topic_storage,
        enrollment_storage,
        user_learning_path_storage,
        user_learning_unit_storage,
):
    return GetUserModuleCompletionPercentageInteractor(
        user_storage=user_storage,
        module_storage=module_storage,
        topic_storage=topic_storage,
        enrollment_storage=enrollment_storage,
        user_learning_path_storage=user_learning_path_storage,
        user_learning_unit_storage=user_learning_unit_storage,
    )


class TestUserModuleCompletionPercentage:

    def test_get_user_module_completion_percentage_successfully(self, interactor,
                                                                snapshot):
        # Act
        result = interactor.get_user_module_completion_percentage(user_id="U001",
                                                                  module_id="M001")

        # Assert
        assert isinstance(result, UserModuleCompletionPercentageDTO)
        assert result.percentage == 70
        snapshot.assert_match(repr(result), "module_completion_success")

    def test_user_not_enrolled_in_module_raises_exception(self, interactor,
                                                          enrollment_storage):
        enrollment_storage.check_user_course_enrollment_exist.return_value = False

        with pytest.raises(UserNotEnrolledInModule):
            interactor.get_user_module_completion_percentage(user_id="U001",
                                                             module_id="M001")

    def test_learning_path_not_found_raises_exception(self, interactor,
                                                      user_learning_path_storage):
        user_learning_path_storage.get_user_learning_path.return_value = None

        with pytest.raises(LearningPathNotFound):
            interactor.get_user_module_completion_percentage(user_id="U001",
                                                             module_id="M001")

    def test_no_learning_units_returns_zero(self, interactor, user_learning_unit_storage):
        user_learning_unit_storage.get_learning_units_by_topic_ids.return_value = []

        result = interactor.get_user_module_completion_percentage(user_id="U001",
                                                                  module_id="M001")

        assert result.percentage == 0

    def test_user_or_module_not_in_db_raises_error(self, interactor, user_storage,
                                                   module_storage):
        user_storage.get_user_ids_in_db.return_value = []
        module_storage.get_db_existing_module_ids.return_value = []
        with pytest.raises(DBNotFoundedModuleIds):
            interactor.get_user_module_completion_percentage(user_id="U001",
                                                             module_id="M001")

        user_storage.check_user_exists.return_value = False
        module_storage.get_db_existing_module_ids.return_value = ["M001"]
        with pytest.raises(UserNotFound):
            interactor.get_user_module_completion_percentage(user_id="U001",
                                                             module_id="M001")
