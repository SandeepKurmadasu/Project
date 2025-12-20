import graphene
from django.contrib.auth import get_user_model, login

from course_management.exceptions.custom_exceptions import ExistedEmailFound, \
    NotExistedEmailFound, WrongPasswordFound
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import ExistingEmail, \
    NotExistedEmailFoundType, WrongPasswordFoundType
from course_management.view_graphql.types.input_types import UserLogInReqParams
from course_management.view_graphql.types.response_type import \
    UserLoginResponse
from course_management.view_graphql.types.types import UserLoginResponseType, \
    UserLoginType


class UserLogInMutation(graphene.Mutation):
    class Arguments:
        params = UserLogInReqParams(required=True)

    Output = UserLoginResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            email = params.email
            password = params.password

            user_storage = UserStorage()
            interactor = UserInteractor(user_storage=user_storage)

            result = interactor.user_login(email=email,password=password)

            request = info.context

            User = get_user_model()
            try:
                user = User.objects.get(id=result.user_id)
            except User.DoesNotExist:
                user = None

            if user:
                login(request, user)

            return UserLoginResponseType(
                token=None,  # no JWT token since session is created
                user=UserLoginType(
                    user_id=str(result.user_id),
                    email=result.email,
                    name=result.name,
                )
            )

        except ExistedEmailFound as e:
            return ExistingEmail(email=e.email)

        except NotExistedEmailFound as e:
            return NotExistedEmailFoundType(email=e.email)

        except WrongPasswordFound as e:
            return WrongPasswordFoundType(password=e.password)
