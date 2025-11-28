from course_management.exceptions.custom_exceptions import \
    ExistedUsernameFound, ExistedEmailFound, \
    ExistedPhoneNumberFound, UsernameNotFound
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.dtos import CreateUserDTO, \
    UserDTO, UpdateUserDTO
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class UserInteractor(ValidationMixIn):
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def create_user(self, user_details: CreateUserDTO) -> UserDTO:
        self._is_username_taken(user_details.username)
        self._is_email_registered(email=user_details.email)
        self._is_phone_number_exists(phone_number=user_details.phone_number)

        return self.user_storage.create_user(user_details=user_details)

    def update_user(self, user_update_data: UpdateUserDTO) -> UserDTO:

        user_id = user_update_data.user_id
        self.check_user_exists(user_id=user_update_data.user_id,
                               user_storage=self.user_storage)
        self._check_updated_username_exist(username=user_update_data.username,user_id=user_id)
        self._check_updated_email_exist(email=user_update_data.email,user_id=user_id)
        self._check_updated_phone_number_exist(user_id=user_id,
            phone_number=user_update_data.phone_number,)

        return self.user_storage.update_user(user_details=user_update_data)

    def get_user_profile(self, user_id: str) -> UserDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.get_user_profile(user_id=user_id)

    def block_user(self, user_id: str) -> UserDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.block_user(user_id=user_id)

    def reset_otp_count(self, user_id: str) -> UserDTO:
        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.reset_otp_count(user_id=user_id)

    def user_login(self, email: str, password: str) -> UserDTO | None:
        self._check_email_exist_or_not(email=email)
        user_data = self.user_storage.get_user_data(email=email)

        if user_data.password == password:
            return user_data
        return None

    def _is_username_taken(self, username: str):
        is_existed_user_name = self.user_storage.check_username_exists(
            username=username)

        if is_existed_user_name:
            raise ExistedUsernameFound(username=username)

    def _is_email_registered(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if is_existed_email:
            raise ExistedEmailFound(email=email)

    def _is_phone_number_exists(self, phone_number: str):
        is_existed_phone_number = self.user_storage.check_phone_number_exists(
            phone_number=phone_number)

        if is_existed_phone_number:
            raise ExistedPhoneNumberFound(phone_number=phone_number)

    def _check_username_exist_or_not(self, username: str):
        is_existed_username = self.user_storage.check_username_exists(
            username=username)

        if not is_existed_username:
            raise UsernameNotFound(username=username)

    def _check_email_exist_or_not(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if not is_existed_email:
            raise ExistedEmailFound(email=email)

    def _check_updated_username_exist(self, username: str, user_id: str):
        is_user_exist_username = self.user_storage.check_user_username_exists(
            user_id=user_id, username=username)

        if not is_user_exist_username:
            self._is_username_taken(username=username)
    def _check_updated_email_exist(self, user_id: str, email: str):

        is_user_exist_email = self.user_storage.check_user_email_exists(
            user_id=user_id, email=email)

        if not is_user_exist_email:
            self._is_email_registered(email=email)

    def _check_updated_phone_number_exist(self, user_id: str,
                                          phone_number: str):

        is_user_exist_phone_number = self.user_storage.check_user_phone_number_exists(
            user_id=user_id, phone_number=phone_number)

        if not is_user_exist_phone_number:
            self._is_phone_number_exists(phone_number=phone_number)


