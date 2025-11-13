from course_management.interactors.dtos import CreateUserDTO, \
    UserDTO, \
    UpdateUserDTO
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from course_management.models import User


class UserStorage(UserStorageInterface):

    def create_user(self, user_details: CreateUserDTO) -> UserDTO:
        user_data = User.objects.create(
            name=user_details.name, username=user_details.username,
            password=user_details.password, email=user_details.email,
            phone_number=user_details.phone_number)

        return UserDTO(
            user_id=user_data.user_id,
            name=user_data.name,
            gender=user_data.gender,
            username=user_data.username,
            password=user_data.password,
            email=user_data.password,
            phone_number=user_data.phone_number,
            is_active=user_data.is_active,
            otp_count=user_data.otp_count
        )

    def check_username_exists(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    def check_email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def check_phone_number_exists(self, phone_number: int) -> bool:
        return User.objects.filter(phone_number=phone_number).exists()

    def check_user_exists(self, user_id: str) -> bool:
        return User.objects.filter(user_id=user_id).exists()

    def update_user(self, user_details: UpdateUserDTO) -> UserDTO:
        user_data = User.objects.get(user_id=user_details.user_id)
        user_data.name = user_details.name
        user_data.username = user_details.username
        user_data.password = user_details.password
        user_data.email = user_details.email
        user_data.phone_number = user_details.phone_number
        user_data.save()

        return UserDTO(
            user_id=user_data.user_id,
            name=user_data.name,
            gender=user_data.gender,
            username=user_data.username,
            password=user_data.password,
            email=user_data.password,
            phone_number=user_data.phone_number,
            is_active=user_data.is_active,
            otp_count=user_data.otp_count
        )

    def get_user_profile(self, user_id: str) -> UserDTO:
        # get user_details
        user_details = User.objects.get(user_id=user_id)

        return UserDTO(
            user_id=user_details.user_id,
            name=user_details.name,
            gender=user_details.gender,
            username=user_details.username,
            password=user_details.password,
            email=user_details.password,
            phone_number=user_details.phone_number,
            is_active=user_details.is_active,
            otp_count=user_details.otp_count
        )

    def block_user(self, user_id: str) -> UserDTO:
        user_data = User.objects.get(user_id=user_id)
        user_data.is_active = False
        user_data.save()

        return UserDTO(
            user_id=user_data.user_id,
            name=user_data.name,
            gender=user_data.gender,
            username=user_data.username,
            password=user_data.password,
            email=user_data.password,
            phone_number=user_data.phone_number,
            is_active=user_data.is_active,
            otp_count=user_data.otp_count
        )

    def reset_otp_count(self, user_id: str) -> UserDTO:
        user_data = User.objects.get(user_id=user_id)
        user_data.otp_count = 0
        user_data.save()

        return UserDTO(
            user_id=user_data.user_id,
            name=user_data.name,
            gender=user_data.gender,
            username=user_data.username,
            password=user_data.password,
            email=user_data.password,
            phone_number=user_data.phone_number,
            is_active=user_data.is_active,
            otp_count=user_data.otp_count
        )
