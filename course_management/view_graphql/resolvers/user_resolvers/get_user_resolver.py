from course_management.exceptions import custom_exceptions
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import UserNotFoundType
from course_management.view_graphql.types.types import UserType


def get_user_profile_resolver(root, info, params):
    user_id = params.user_id

    user_storage = UserStorage()
    interactor = UserInteractor(user_storage=user_storage)

    try:
        user_data = interactor.get_user_profile(user_id=user_id)

        user_output = UserType(
            user_id=params.user_id,
            name=user_data.name,
            gender=user_data.gender,
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            phone_number=user_data.phone_number,
            is_active=user_data.is_active,
            otp_count=user_data.otp_count,
        )

        return user_output

    except custom_exceptions.UserNotFound as e:
        return UserNotFoundType(
            user_id=e.user_id
        )
