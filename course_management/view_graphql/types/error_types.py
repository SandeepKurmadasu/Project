import graphene


class DuplicateTitlesInRequest(graphene.ObjectType):
    titles = graphene.List(graphene.String, required=True)


class TitleAlreadyExistsInDB(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class InvalidLevelType(graphene.ObjectType):
    level_types = graphene.List(graphene.String, required=True)


class DuplicateCourseIdsInRequest(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class CourseIdsNotFound(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class ExistingUserName(graphene.ObjectType):
    username = graphene.String(required=True)


class ExistingEmail(graphene.ObjectType):
    email = graphene.String(required=True)


class NotExistedEmailFoundType(graphene.ObjectType):
    email = graphene.String(required=True)


class WrongPasswordFoundType(graphene.ObjectType):
    password = graphene.String(required=True)


class ExistingPhoneNumber(graphene.ObjectType):
    phone_number = graphene.String(required=True)


class NotExistingTopicTypes(graphene.ObjectType):
    topic_types = graphene.List(graphene.String, required=True)


class TopicIdsNotFound(graphene.ObjectType):
    topic_ids = graphene.List(graphene.String, required=True)


class TopicNotFound(graphene.ObjectType):
    topic_id = graphene.String(required=True)


class CheckCourseFound(graphene.ObjectType):
    course_id = graphene.String()


class CheckUserFound(graphene.ObjectType):
    user_id = graphene.String()


class CourseIdsNotInDB(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class DuplicateCourseIdsFoundType(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class UserNotFoundType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class CourseNotFoundType(graphene.ObjectType):
    course_id = graphene.String(required=True)


class ModuleIdsNotFoundInDBType(graphene.ObjectType):
    module_ids = graphene.List(graphene.String, required=True)


class DuplicateCourseTitlesFoundType(graphene.ObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class AlreadyExistedTitlesFoundType(graphene.ObjectType):
    module_ids = graphene.List(graphene.String, required=True)


class DuplicateTitlesFoundType(graphene.ObjectType):
    titles = graphene.List(graphene.String, required=True)


class UnexpectedLevelTypeFoundType(graphene.ObjectType):
    level_types = graphene.List(graphene.String, required=True)


class UserNotEnrolledCourseType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class NotExistingTopicTypesFoundType(graphene.ObjectType):
    topic_types = graphene.List(graphene.String, required=True)


class NotExistingTopicIdsFoundType(graphene.ObjectType):
    topic_ids = graphene.List(graphene.String, required=True)


class NotExistedTopicFoundType(graphene.ObjectType):
    topic_id = graphene.String(required=True)


class ExistedUsernameFoundType(graphene.ObjectType):
    username = graphene.String(required=True)


class ExistedEmailFoundType(graphene.ObjectType):
    email = graphene.String(required=True)


class ExistedPhoneNumberFoundType(graphene.ObjectType):
    phone_number = graphene.String(required=True)


class UsernameNotFoundType(graphene.ObjectType):
    username = graphene.String(required=True)


class CourseInProgressExceptionType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class UserNotEnrolledInModuleType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class UserLearningPathNotFoundType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)


class LearningUnitIdNotFoundType(graphene.ObjectType):
    learning_unit_id = graphene.String(required=True)


class UserLearningUnitIdNotFoundType(graphene.ObjectType):
    user_learning_unit_id = graphene.Int(required=True)


class LearningUnitLockedExceptionType(graphene.ObjectType):
    user_learning_unit_id = graphene.Int(required=True)


class LearningPathNotFoundType(graphene.ObjectType):
    course_id = graphene.String(required=True)


class UserLearningPathIdNotFoundType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)



