from unittest.mock import MagicMock

import pytest
from faker import Faker

from course_management.exceptions.custom_exceptions import \
    ExistedUsernameFound, ExistedPhoneNumberFound, ExistedEmailFound
from course_management.interactors.dtos import CreateUserDTO, GenderEnum
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage

Faker.seed()


class TestCreateUser:

    @pytest.mark.django_db
    def test_create_user_successfully(self, snapshot):
        # Arrange

        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        user_input_data = CreateUserDTO(
            name="Name",
            username='Username',
            password="Baba!2#4",
            phone_number="9815267845",
            email="babahajvali@gmail.com",
            gender=GenderEnum.MALE
        )

        # ACT

        result = interactor.create_user(user_details=user_input_data)

        # Assert
        snapshot.assert_match(repr(result.email),
                              "test_create_user_successfully.txt")

    @pytest.mark.django_db
    def test_create_user_raises_username_exception(self, snapshot):
        # Arrange

        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)
        user_storage.check_username_exists = MagicMock(return_value=True)

        user_input_data = CreateUserDTO(
            name="Name",
            username='Username',
            password="Baba!2#4",
            phone_number="9815267845",
            email="babahajvali@gmail.com",
            gender=GenderEnum.MALE
        )

        # ACT
        with pytest.raises(ExistedUsernameFound) as e:
            interactor.create_user(user_input_data)

        # Assert
        snapshot.assert_match(repr(e.value.username),
                              "test_create_user_raises_username_exception.txt")

    @pytest.mark.django_db
    def test_create_user_raises_email_exception(self, snapshot):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        user_storage.check_email_exists = MagicMock(return_value=True)
        user_storage.is_phone_number_exists = MagicMock(return_value=False)
        user_storage.is_username_taken = MagicMock(return_value=False)

        user_details = CreateUserDTO(
            name="Name",
            username='NewUsername1',
            password="Baba!2#4",
            phone_number="9815267845",
            email="existingemail@example.com",
            gender=GenderEnum.MALE
        )

        with pytest.raises(ExistedEmailFound) as exc_info:
            interactor.create_user(user_details)

        snapshot.assert_match(repr(exc_info.value),
                              "test_create_user_raises_email_exception.txt")

    @pytest.mark.django_db
    def test_create_user_raises_phone_exception(self, snapshot):
        user_storage = UserStorage()
        user_storage.is_username_taken = MagicMock(return_value=False)
        user_storage.is_email_registered = MagicMock(return_value=False)
        user_storage.check_phone_number_exists = MagicMock(
            return_value=True)

        interactor = UserInteractor(user_storage=user_storage)

        user_details = CreateUserDTO(
            name="Name",
            username='NewUsername2',
            password="Baba!2#4",
            phone_number="existingphone",
            email="newemail@example.com",
            gender=GenderEnum.MALE
        )

        with pytest.raises(ExistedPhoneNumberFound) as exc_info:
            interactor.create_user(user_details)

        snapshot.assert_match(str(exc_info.value),
                              "test_create_user_raises_phone_exception.txt")

