import json
import pytest
from unittest.mock import Mock

from course_management.interactors.user.user_interactor import UserInteractor
from course_management.interactors.dtos import UpdateUserDTO, UserDTO, GenderEnum
from course_management.exceptions.custom_exceptions import (
    ExistedUsernameFound,
    ExistedEmailFound,
    ExistedPhoneNumberFound,
    UserNotFound,
)


@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def interactor(user_storage):
    return UserInteractor(user_storage=user_storage)


@pytest.mark.django_db
class TestUpdateUser:

    def test_update_user_success(self, interactor, user_storage, snapshot):

        update_data = UpdateUserDTO(
            user_id="U001",
            name="Baba",
            gender=GenderEnum.MALE,
            username="Baba123",
            password="BabaH123",
            email="baba@example.com",
            phone_number=9812347650,
        )

        user_storage.check_user_exists.return_value = True
        user_storage.check_username_exists.return_value = False
        user_storage.check_email_exists.return_value = False
        user_storage.check_phone_number_exists.return_value = False

        expected = UserDTO(
            user_id="U001",
            name="Sandy",
            gender=GenderEnum.MALE,
            username="Sandy123",
            password="SandyK123",
            email="Sandy@example.com",
            phone_number=9174274893,
            is_active=True,
            otp_count=0,
        )

        user_storage.update_user.return_value = expected

        result = interactor.update_user(update_data)

        snapshot.assert_match(
            repr(result),
            "update_user_success_snapshot.json"
        )

    def test_update_user_not_found(self, interactor, user_storage, snapshot):
        update_data = UpdateUserDTO(
            user_id="U404",
            name="User",
            gender=GenderEnum.MALE,
            username="user",
            password="pass123",
            email="user@example.com",
            phone_number=1112223333,
        )

        user_storage.check_user_exists.return_value = False

        with pytest.raises(UserNotFound) as exc:
            interactor.update_user(update_data)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "update_user_not_found_snapshot.json",
        )

    def test_update_user_username_exists(self, interactor, user_storage, snapshot):
        update_data = UpdateUserDTO(
            user_id="U001",
            name="John",
            gender=GenderEnum.MALE,
            username="taken_username",
            password="secret123",
            email="john@example.com",
            phone_number=9876543210,
        )

        user_storage.check_user_exists.return_value = True
        user_storage.check_user_username_exists.return_value = False  # ← ADD THIS
        user_storage.check_username_exists.return_value = True

        with pytest.raises(ExistedUsernameFound) as exc:
            interactor.update_user(update_data)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "update_user_username_exists_snapshot.json",
        )

    def test_update_user_email_exists(self, interactor, user_storage, snapshot):
        update_data = UpdateUserDTO(
            user_id="U001",
            name="John",
            gender=GenderEnum.MALE,
            username="john123",
            password="secret123",
            email="taken@example.com",
            phone_number=9876543210,
        )

        user_storage.check_user_exists.return_value = True
        user_storage.check_username_exists.return_value = False
        user_storage.check_user_username_exists.return_value = True  # ← ADD THIS
        user_storage.check_user_email_exists.return_value = False  # ← ADD THIS
        user_storage.check_email_exists.return_value = True

        with pytest.raises(ExistedEmailFound) as exc:
            interactor.update_user(update_data)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "update_user_email_exists_snapshot.json",
        )

    def test_update_user_phone_exists(self, interactor, user_storage, snapshot):
        update_data = UpdateUserDTO(
            user_id="U001",
            name="John",
            gender=GenderEnum.MALE,
            username="john123",
            password="secret123",
            email="john@example.com",
            phone_number=9999999999,
        )

        user_storage.check_user_exists.return_value = True
        user_storage.check_username_exists.return_value = False
        user_storage.check_user_username_exists.return_value = True  # ← ADD THIS
        user_storage.check_email_exists.return_value = False
        user_storage.check_user_email_exists.return_value = True  # ← ADD THIS
        user_storage.check_phone_number_exists.return_value = True
        user_storage.check_user_phone_number_exists.return_value = False  # ← ADD THIS

        with pytest.raises(ExistedPhoneNumberFound) as exc:
            interactor.update_user(update_data)

        snapshot.assert_match(
            json.dumps({"error": str(exc.value)}, indent=2),
            "update_user_phone_exists_snapshot.json",
        )
