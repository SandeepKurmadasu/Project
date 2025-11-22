import graphene
from ..types.input_types import CreateUserInput
from ..types.types import UserType

from course_management.interactors.user.user_interactor import UserInteractor, CreateUserDTO
from course_management.storages.user_storage import UserStorage
from course_management.exceptions.custom_exceptions import (
ExistedUsernameFound,
ExistedEmailFound,
ExistedPhoneNumberFound,
)
from ..types.error_types import (
    ExistingEmail,
    ExistingUserName,
    ExistingPhoneNumber
)
from course_management.graphql.types.response_types import CreateUserResponse

class CreateUser(graphene.Mutation):
    class Arguments:
        user = graphene.Argument(CreateUserInput, required=True)

    Output = CreateUserResponse

    @staticmethod
    def mutate(root, info, user):
        from course_management.models import User as DjangoUser

        try:
            dto =CreateUserDTO(
                    name=user.name,
                    username=user.username,
                    password=user.password,
                    gender=DjangoUser.GenderEnum(user.gender),
                    email=user.email,
                    phone_number=user.phone_number
                )

            created_dto = UserInteractor(user_storage=UserStorage()).create_user(dto)

            return UserType(
                    user_id= created_dto.user_id,
                    name =created_dto.name,
                    gender = created_dto.gender,
                    username =  created_dto.username,
                    email = created_dto.email,
                    phone_number = created_dto.phone_number,
                    is_active = created_dto.is_active,
                    otp_count = created_dto.otp_count
            )

        except ExistedUsernameFound as e:
            return ExistingUserName(username=e.username)
        except ExistedEmailFound as e:
            return ExistingEmail(email=e.email)
        except ExistedPhoneNumberFound as e:
            return ExistingPhoneNumber(phone_number=e.phone_number)
