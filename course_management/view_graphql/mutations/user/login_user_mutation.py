import graphene

from course_management.exceptions.custom_exceptions import EmailNotFound, WrongPassword
from course_management.interactors.user.user_interactor import UserInteractor
from course_management.storages.user_storage import UserStorage
from course_management.view_graphql.types import UserType


class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, email, password):
        interactor = UserInteractor(user_storage=UserStorage())

        try:
            user_dto = interactor.user_login(email=email, password=password)

            return LoginUser(
                success=True,
                message="Login successful!",
                user=UserType(
                    user_id=user_dto.user_id,
                    name=user_dto.name,
                    username=user_dto.username,
                    email=user_dto.email,
                    phone_number=user_dto.phone_number,
                    gender=user_dto.gender,
                    is_active=user_dto.is_active,
                )
            )
        except (EmailNotFound, WrongPassword):
            return LoginUser(
                success=False,
                message="Invalid email or password",
                user=None
            )