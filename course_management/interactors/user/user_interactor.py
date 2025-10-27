from course_management.exceptions.custom_exceptions import ExistedUsernameFound, ExistedEmailFound, \
    ExistedPhoneNumberFound, UsernameNotFound
from course_management.interactors.validations import ValidationMixIns
from course_management.interactors.dtos import CreateUserDTO, UserDTO, UpdateUserDTO
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface


class UserInteractor(ValidationMixIns):
    def __init__(self,user_storage : UserStorageInterface):
        self.user_storage = user_storage

    def create_user(self,user_details : CreateUserDTO)->UserDTO:
        self._is_username_taken(user_details.username)
        self._is_email_registered(email=user_details.email)
        self._is_phone_number_exists(phone_number=user_details.phone_number)

        return self.user_storage.create_user(user_details=user_details)

    def update_user(self,user_update_data : UpdateUserDTO)-> UserDTO:
        self.check_if_user_exists(user_id=user_update_data.user_id, user_storage= self.user_storage)
        self._is_username_taken(username=user_update_data.username)
        self._is_email_registered(email=user_update_data.email)
        self._is_phone_number_exists(phone_number=user_update_data.phone_number)

        return self.user_storage.update_user(user_details=user_update_data)

    def get_user_profile(self,user_id : str)->UserDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.get_user_profile(user_id=user_id)

    def block_user(self,user_id : str)->UserDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.block_user(user_id=user_id)

    def reset_otp_count(self,user_id : str)->UserDTO:
        self.check_if_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.reset_otp_count(user_id=user_id)


    def _is_username_taken(self, username :str):
        is_existed_user_name = self.user_storage.check_username_exists(username=username)

        if is_existed_user_name:
            raise ExistedUsernameFound(username=username)

    def _is_email_registered(self, email : str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if is_existed_email:
            raise ExistedEmailFound(email=email)

    def _is_phone_number_exists(self,phone_number : int):
        is_existed_phone_number = self.user_storage.check_phone_number_exists(phone_number=phone_number)

        if is_existed_phone_number:
            raise ExistedPhoneNumberFound(phone_number=phone_number)

    def _check_username_exist_or_not(self,username : str):
        is_existed_username = self.user_storage.check_username_exists(username=username)

        if not is_existed_username:
            raise UsernameNotFound(username=username)