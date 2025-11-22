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
    username=graphene.String(required=True)


class ExistingEmail(graphene.ObjectType):
    email=graphene.String(required=True)


class ExistingPhoneNumber(graphene.ObjectType):
    phone_number=graphene.String(required=True)


class NotExistingTopicTypes(graphene.ObjectType):
    topic_types=graphene.List(graphene.String,required=True)


class TopicIdsNotFound(graphene.ObjectType):
    topic_ids = graphene.List(graphene.String, required=True)


class CheckCourseFound(graphene.ObjectType):
    course_id = graphene.String()


class CheckUserFound(graphene.ObjectType):
    user_id = graphene.String()