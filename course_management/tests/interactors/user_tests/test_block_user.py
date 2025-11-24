import pytest
from unittest.mock import Mock

from course_management.interactors.user.user_interactor import UserInteractor
from course_management.interactors.dtos import UserDTO, GenderEnum


@pytest.fixture
def user_storage():
    return Mock()


@pytest.fixture
def interactor(user_storage):
    return UserInteractor(user_storage=user_storage)


@pytest.mark.django_db
def test_block_user_success(interactor, user_storage, snapshot):
    user_storage.check_user_exists.return_value = True

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

    user_storage.block_user.return_value = expected

    result = interactor.block_user("U001")

    snapshot.assert_match(repr(result), "block_user_success.json")
