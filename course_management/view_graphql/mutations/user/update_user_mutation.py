import uuid

import graphene

from course_management.exceptions import custom_exceptions
from course_management.interactors.dtos import UpdateUserDTO
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType, \
    ExistedUsernameFoundType, ExistedEmailFoundType, \
    ExistedPhoneNumberFoundType
from course_management.view_graphql.types.input_types import \
    UpdateUserReqParams
from course_management.view_graphql.types.response_type import UserResponse
from course_management.view_graphql.types.types import UserType


class UpdateUser(graphene.Mutation):
    class Arguments:
        params = UpdateUserReqParams(required=True)

    Output = UserResponse

    @staticmethod
    def mutate(root,info,params):

        input_data = UpdateUserDTO(
            user_id=params.user_id,
            name=params.name,
            gender=params.gender,
            username=params.username,
            password=params.password,
            email=params.email,
            phone_number=params.phone_number
        )

        user_storage = UserStorage()

        interactor = UserInteractor(user_storage=user_storage)

        try:
            user_data = interactor.update_user(user_update_data=input_data)

            user_output = UserType(
                user_id=params.user_id,
                name=user_data.name,
                gender =user_data.gender,
                username = user_data.username,
                password = user_data.password,
                email = user_data.email,
                phone_number = user_data.phone_number,
                is_active = user_data.is_active,
                otp_count = user_data.otp_count,
            )

            return user_output

        except custom_exceptions.UserNotFound as e:
            return UserNotFoundType(
                user_id=e.user_id
            )

        except custom_exceptions.ExistedUsernameFound as e:
            return ExistedUsernameFoundType(
                username=e.username
            )

        except custom_exceptions.ExistedEmailFound as e:
            return ExistedEmailFoundType(
                email=e.email
            )

        except custom_exceptions.ExistedPhoneNumberFound as e:
            return ExistedPhoneNumberFoundType(
                phone_number=e.phone_number
            )