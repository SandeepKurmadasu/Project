from course_management.interactors.dtos import \
    UserLearningPathDTO
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.models import UserLearningPath, User, \
    CourseLearningPath, LearningUnit


class UserLearningPathStorage(UserLearningPathStorageInterface):
    def get_user_learning_path(self, user_id: str,
                               course_id: str) -> UserLearningPathDTO:

        user_learning_path = (
            UserLearningPath.objects.filter(user_id=user_id,
                                            learning_path__course_id=course_id)
            .order_by("-created_at").first()
        )

        return UserLearningPathDTO(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            user_id=user_learning_path.user.user_id,
            learning_path_id=user_learning_path.learning_path.learning_path_id,
            current_learning_unit_id=user_learning_path.current_learning_unit.pk,
            overall_percentage=user_learning_path.overall_percentage,
            status=user_learning_path.status,
        )

    def get_user_learning_path_with_id(self, user_id: str,
                                       learning_path_id: str) -> UserLearningPathDTO | None:
        user_learning_path = UserLearningPath.objects.filter(
            user_id=user_id, learning_path_id=learning_path_id).first()

        if not user_learning_path:
            return None

        return UserLearningPathDTO(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            user_id=user_learning_path.user.user_id,
            learning_path_id=user_learning_path.learning_path.learning_path_id,
            current_learning_unit_id=user_learning_path.current_learning_unit.pk,
            overall_percentage=user_learning_path.overall_percentage,
            status=user_learning_path.status,
        )

    def create_user_learning_path(
            self, user_id: str,
            course_learning_path_id: str) -> UserLearningPathDTO:
        user = User.objects.get(user_id=user_id)
        course_learning_path = CourseLearningPath.objects.get(
            learning_path_id=course_learning_path_id)

        learning_unit = LearningUnit.objects.get(learning_path_id= course_learning_path_id,order=1)


        user_learning_path = UserLearningPath.objects.create(
            user=user,
            learning_path=course_learning_path,
            current_learning_unit=learning_unit,
            overall_percentage=0,
        )

        return UserLearningPathDTO(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            user_id=user_learning_path.user.user_id,
            learning_path_id=user_learning_path.learning_path.learning_path_id,
            current_learning_unit_id=user_learning_path.current_learning_unit.pk,
            overall_percentage=user_learning_path.overall_percentage,
            status=user_learning_path.status,
        )

    def get_user_learning_path_with_user_learning_path_id(
            self, user_learning_path_id: str) -> UserLearningPathDTO:
        user_learning_path = (UserLearningPath.objects.filter(
            user_learning_path_id=user_learning_path_id).first())

        return UserLearningPathDTO(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            user_id=user_learning_path.user.user_id,
            learning_path_id=user_learning_path.learning_path.learning_path_id,
            current_learning_unit_id=user_learning_path.current_learning_unit.pk,
            overall_percentage=user_learning_path.overall_percentage,
            status=user_learning_path.status,
        )

    def check_user_learning_path_exists(self,
                                        user_learning_path_id: str) -> bool:
        return UserLearningPath.objects.filter(
            user_learning_path_id=user_learning_path_id).exists()

    def update_user_learning_path_percentage(
            self, user_learning_path_id: str, percentage: int) \
            -> UserLearningPathDTO:
        user_learning_path = UserLearningPath.objects.get(
            user_learning_path_id=user_learning_path_id)
        user_learning_path.overall_percentage = percentage
        user_learning_path.save(
            update_fields=["overall_percentage", "updated_at"])

        return UserLearningPathDTO(
            user_learning_path_id=user_learning_path.user_learning_path_id,
            user_id=user_learning_path.user.user_id,
            learning_path_id=user_learning_path.learning_path.learning_path_id,
            current_learning_unit_id=user_learning_path.current_learning_unit.pk,
            overall_percentage=user_learning_path.overall_percentage,
            status=user_learning_path.status,
        )
