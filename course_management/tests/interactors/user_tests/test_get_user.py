import pytest
from unittest.mock import MagicMock

from course_management.exceptions.custom_exceptions import UserNotFound
from course_management.interactors.dtos import UserDTO, GenderEnum
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage

class TestUserInteractorGetUserProfile:

    def test_get_user_profile_success(self,snapshot):
        # Arrange
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        # Mock check_user_exists to do nothing (pass)
        interactor.check_user_exists = MagicMock()

        # Mock get_user_profile to return a dummy UserDTO
        expected_user = UserDTO(
            user_id="123",
            name="John Doe",
            username="johndoe",
            email="john@example.com",
            phone_number="1234567890",
            gender=GenderEnum.MALE,
            is_active=True,
            otp_count=0,
            password="Baba1234"
        )
        user_storage.get_user_profile = MagicMock(return_value=expected_user)

        # Act
        result = interactor.get_user_profile(user_id="123")

        # Assert
        snapshot.assert_match(repr(result),"test_get_user_successfully.txt")

    def test_get_user_profile_user_not_found(self,snapshot):
        # Arrange
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        interactor.check_user_exists = MagicMock(side_effect=UserNotFound("User not found"))

        with pytest.raises(UserNotFound) as exc_info:
            interactor.get_user_profile(user_id="999")


        snapshot.assert_match(repr(exc_info.value),"test_get_user_successfully.txt")
