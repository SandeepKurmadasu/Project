import graphene

from course_management.exceptions import custom_exceptions
from course_management.interactors.learning_path.generate_learning_path_for_course import \
    GenerateLearningPathForCourseInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.learning_path_storage import LearningPathStorage
from course_management.storages.learning_unit_storage import LearningUnitStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage

from course_management.view_graphql.types.error_types import CourseNotFoundType
from course_management.view_graphql.types.input_types import \
    GenerateCourseLearningPathReqParams
from course_management.view_graphql.types.response_type import LearningPathResponse
from course_management.view_graphql.types.types import LearningUnitType, LearningPathType


class GenerateCourseLearningPathMutation(graphene.Mutation):
    class Arguments:
        params = GenerateCourseLearningPathReqParams(required=True)

    Output = LearningPathResponse

    @staticmethod
    def mutate(root, info, params):
        course_id = params.course_id

        course_storage = CourseStorage()
        module_storage = ModuleStorage()
        topic_storage = TopicStorage()
        learning_path_storage = LearningPathStorage()
        learning_unit_storage = LearningUnitStorage()

        interactor = GenerateLearningPathForCourseInteractor(
            course_storage=course_storage,
            module_storage=module_storage,
            topic_storage=topic_storage,
            learning_path_storage=learning_path_storage,
            learning_unit_storage=learning_unit_storage,
        )

        try:
            learning_path_dto = interactor.generate_learning_path_for_course(
                course_id=course_id
            )

            units = []
            if learning_path_dto.learning_units:
                for u in learning_path_dto.learning_units:
                    units.append(
                        LearningUnitType(
                            learning_unit_id=u.learning_unit_id,
                            learning_path_id=u.learning_path_id,
                            unit_type=u.unit_type,
                            topic_id=u.topic_id,
                            unit_title=u.unit_title,
                            order=u.order,
                            estimated_duration_in_minutes=u.estimated_duration_in_minutes,
                        )
                    )

            return LearningPathType(
                learning_path_id=learning_path_dto.learning_path_id,
                course_id=learning_path_dto.course_id,
                course_title=learning_path_dto.course_title,
                total_units=learning_path_dto.total_units,
                estimated_total_duration_in_minutes=learning_path_dto.estimated_total_duration_in_minutes,
                learning_units=units,
            )

        except custom_exceptions.CourseNotFound as e:
            return CourseNotFoundType(course_id=e.course_id)
