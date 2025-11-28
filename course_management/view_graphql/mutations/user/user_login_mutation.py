import graphene
from datetime import datetime, timedelta
from django.conf import settings
import jwt

from course_management.exceptions.custom_exceptions import ExistedEmailFound
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types.error_types import ExistingEmail
from course_management.view_graphql.types.input_types import UserLogInReqParams
from course_management.view_graphql.types.response_type import \
    UserLoginResponse
from course_management.view_graphql.types.types import UserLoginResponseType, \
    UserLoginType

def create_token(payload):
    """Create a JWT token"""
    try:
        token_payload = {
            **payload,
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }

        if 'userId' in token_payload:
            token_payload['userId'] = str(token_payload['userId'])

        secret_key = settings.SECRET_KEY
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        print(f"ERROR in create_token: {type(e).__name__}: {str(e)}")
        raise


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

            result = interactor.user_login(
                email=email,
                password=password
            )

            token = create_token({"userId": str(result.user_id)})

            return UserLoginResponseType(
                token=token,
                user=UserLoginType(
                    user_id=str(result.user_id),
                    email=result.email,
                    name=result.name,
                )
            )

        except ExistedEmailFound as e:
            return ExistingEmail(email=e.email)
