import pytest
from unittest.mock import create_autospec, MagicMock, patch
from dataclasses import dataclass

from course_management.exceptions.custom_exceptions import (
    UserLearningPathNotFound,
    LearningUnitIdNotFound,
    LearningUnitLockedException,
)
from course_management.interactors.dtos import \
    AttemptedTopicStatusEnum
from course_management.interactors.learning_path.update_learning_unit_progress_status import (
    UpdateLearningUnitProgressStatusInteractor,
)
from course_management.interactors.storage_interfaces.learning_path_storage_interface import (
    LearningPathStorageInterface,
)
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import (
    LearningUnitStorageInterface,
)
from course_management.interactors.storage_interfaces.user_learning_path import (
    UserLearningPathStorageInterface,
)
from course_management.interactors.storage_interfaces.user_learning_units_storage_interface import (
    UserLearningUnitStorageInterface,
)


@dataclass
class MockLearningUnitProgress:
    percentage: int
    is_locked: bool


@dataclass
class MockLearningUnit:
    learning_unit_id: str
    order: int
    learning_path_id: str


@pytest.fixture
def storages():
    return {
        "learning_path_storage": create_autospec(LearningPathStorageInterface),
        "user_learning_storage": create_autospec(
            UserLearningPathStorageInterface),
        "learning_unit_storage": create_autospec(LearningUnitStorageInterface),
        "user_learning_units_storage": create_autospec(
            UserLearningUnitStorageInterface),
    }


@pytest.fixture
def interactor(storages):
    return UpdateLearningUnitProgressStatusInteractor(
        user_learning_storage=storages["user_learning_storage"],
        user_learning_units_storage=storages["user_learning_units_storage"],
    )


@pytest.fixture
def ids():
    return {
        "path_id": "ulp-101",
        "unit_id": "lu-001",
    }


def test_update_learning_unit_progress_status_success(interactor, storages,
                                                      ids, snapshot):
    """✅ Should update learning unit progress successfully."""
    interactor.validate_user_learning_path_exists = MagicMock()
    interactor._validate_learning_unit_belongs_to_path = MagicMock()
    interactor._validate_learning_unit_exists = MagicMock()
    interactor._check_learning_unit_locked = MagicMock()
    interactor._calculate_overall_path_percentage = MagicMock(return_value=80)

    storages[
        "user_learning_units_storage"].update_learning_unit_progress.return_value = None
    storages[
        "user_learning_storage"].update_user_learning_path_percentage.return_value = None

    result = interactor.update_learning_unit_progress_status(
        user_learning_path_id=ids["path_id"],
        user_learning_unit_id=1,
        status=AttemptedTopicStatusEnum.HALF_COMPLETED,
        percentage=60,
    )

    snapshot.assert_match(
        repr(result),
        "update_learning_unit_progress_status_success_snapshot.json",
    )


def test_user_learning_path_not_found(interactor, ids, snapshot):
    with patch(
            "course_management.interactors.common_validation_mixin.ValidationMixIn.validate_user_learning_path_exists",
            side_effect=UserLearningPathNotFound(
                user_learning_path_id=ids["path_id"]),
    ):
        with pytest.raises(UserLearningPathNotFound) as exc:
            interactor.update_learning_unit_progress_status(
                user_learning_path_id=ids["path_id"],
                user_learning_unit_id=1,
                status=AttemptedTopicStatusEnum.START,
                percentage=10,
            )

    snapshot.assert_match(
        repr(exc.value.user_learning_path_id),
        "user_learning_path_not_found_snapshot.txt",
    )




def test_learning_unit_locked_exception(interactor, storages, ids, snapshot):
    interactor.validate_user_learning_path_exists = MagicMock()
    interactor._validate_learning_unit_belongs_to_path = MagicMock()
    interactor._validate_learning_unit_exists = MagicMock()

    interactor._check_learning_unit_locked = MagicMock()
    interactor._check_learning_unit_locked.side_effect = LearningUnitLockedException(
        learning_unit_id=ids["unit_id"]
    )
    storages["user_learning_units_storage"].get_user_learning_unit_progress.return_value = (
        MockLearningUnitProgress(percentage=0, is_locked=True)
    )

    storages["user_learning_units_storage"].get_all_user_learning_unit_progress.return_value = [
        MockLearningUnitProgress(percentage=0, is_locked=True)
    ]

    with pytest.raises(LearningUnitLockedException) as exc:
        interactor.update_learning_unit_progress_status(
            user_learning_path_id=ids["path_id"],
            user_learning_unit_id=1,
            status=AttemptedTopicStatusEnum.START,
            percentage=20,
        )

    snapshot.assert_match(
        repr(exc.value.learning_unit_id),
        "learning_unit_locked_snapshot.txt",
    )



def test_complete_status_unlocks_next_unit(interactor, storages, ids,
                                           snapshot):
    interactor.validate_user_learning_path_exists = MagicMock()
    interactor._validate_learning_unit_belongs_to_path = MagicMock()
    interactor._validate_learning_unit_exists = MagicMock()
    interactor._check_learning_unit_locked = MagicMock()
    interactor._calculate_overall_path_percentage = MagicMock(return_value=100)

    interactor._unlock_next_learning_unit = MagicMock(return_value="lu-002")

    result = interactor.update_learning_unit_progress_status(
        user_learning_path_id=ids["path_id"],
        user_learning_unit_id=1,
        status=AttemptedTopicStatusEnum.COMPLETE,
        percentage=100,
    )

    snapshot.assert_match(
        repr(result),
        "complete_status_unlocks_next_unit_snapshot.json",
    )


def test_calculate_overall_path_percentage_empty(interactor):
    interactor.user_learning_units_storage.get_all_user_learning_unit_progress.return_value = []
    percentage = interactor._calculate_overall_path_percentage("ulp-101")

    assert percentage == 0


def test_calculate_overall_path_percentage_non_empty(interactor):
    interactor.user_learning_units_storage.get_all_user_learning_unit_progress.return_value = [
        MockLearningUnitProgress(percentage=100, is_locked=False),
        MockLearningUnitProgress(percentage=50, is_locked=False),
        MockLearningUnitProgress(percentage=0, is_locked=False),
    ]

    percentage = interactor._calculate_overall_path_percentage("ulp-101")
    assert percentage == 50
