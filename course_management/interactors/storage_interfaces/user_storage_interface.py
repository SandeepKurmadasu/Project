from abc import ABC, abstractmethod

from course_management.interactors.dtos import CreateUserDTO, \
    UserDTO, \
    UpdateUserDTO


class UserStorageInterface(ABC):

    @abstractmethod
    def create_user(self, user_details: CreateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def check_username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def check_email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def check_phone_number_exists(self, phone_number: int) -> bool:
        pass

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def update_user(self, user_details: UpdateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def get_user_profile(self, user_id: str) -> UserDTO:
        pass

    @abstractmethod
    def block_user(self, user_id: str) -> UserDTO:
        pass

    @abstractmethod
    def reset_otp_count(self, user_id: str) -> UserDTO:
        pass
