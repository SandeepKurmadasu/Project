import json
import pytest

from course_management.storages.user_storage import UserStorage
from course_management.interactors.dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    GenderEnum,
)
from course_management.models import User


def dto_to_json(dto):
    d = dto.__dict__.copy()
    d["user_id"] = "STATIC-USER-ID"
    return d


@pytest.mark.django_db
def test_create_user(snapshot):
    storage = UserStorage()

    dto = CreateUserDTO(
        name="John Doe",
        username="john123",
        password="secret",
        gender=GenderEnum.MALE,
        email="john@example.com",
        phone_number=9999999999,
    )

    result = storage.create_user(dto)

    snapshot.assert_match(
        json.dumps(dto_to_json(result), indent=2, sort_keys=True),
        "create_user",
    )


@pytest.mark.django_db
def test_update_user(snapshot):
    user = User.objects.create(
        name="Old Name",
        username="old_user",
        password="old_pass",
        gender="MALE",
        email="old@example.com",
        phone_number=80808080,
    )

    storage = UserStorage()

    dto = UpdateUserDTO(
        user_id=str(user.user_id),
        name="New Name",
        gender=GenderEnum.FEMALE,
        username="new_user",
        password="new_pass",
        email="new@example.com",
        phone_number=1234567890,
    )

    result = storage.update_user(dto)

    snapshot.assert_match(
        json.dumps(dto_to_json(result), indent=2, sort_keys=True),
        "update_user",
    )

    user.refresh_from_db()
    assert user.name == "New Name"
    assert user.gender == "FEMALE"
    assert user.username == "new_user"
    assert user.email == "new@example.com"


@pytest.mark.django_db
def test_get_user_profile(snapshot):
    user = User.objects.create(
        name="Test User",
        username="tester",
        password="test123",
        gender="MALE",
        email="t@test.com",
        phone_number=12345,
    )

    storage = UserStorage()
    result = storage.get_user_profile(str(user.user_id))

    snapshot.assert_match(
        json.dumps(dto_to_json(result), indent=2, sort_keys=True),
        "get_user_profile",
    )


@pytest.mark.django_db
def test_block_user(snapshot):
    user = User.objects.create(
        name="Active User",
        username="active_user",
        password="pass",
        gender="MALE",
        email="a@a.com",
        phone_number=123,
        is_active=True,
    )

    storage = UserStorage()
    result = storage.block_user(str(user.user_id))

    snapshot.assert_match(
        json.dumps(dto_to_json(result), indent=2, sort_keys=True),
        "block_user",
    )

    user.refresh_from_db()
    assert user.is_active is False


@pytest.mark.django_db
def test_reset_otp_count(snapshot):
    user = User.objects.create(
        name="OTP User",
        username="otp_user",
        password="otp123",
        gender="MALE",
        email="otp@x.com",
        phone_number=8888,
        otp_count=10,
    )

    storage = UserStorage()
    result = storage.reset_otp_count(str(user.user_id))

    snapshot.assert_match(
        json.dumps(dto_to_json(result), indent=2, sort_keys=True),
        "reset_otp_count",
    )

    user.refresh_from_db()
    assert user.otp_count == 0
