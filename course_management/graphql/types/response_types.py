import graphene

from .types import CoursesType, UserType, TopicsType, CourseFeedbackType
from .error_types import (
    DuplicateTitlesInRequest,
    TitleAlreadyExistsInDB,
    InvalidLevelType,
    DuplicateCourseIdsInRequest,
    CourseIdsNotFound, ExistingEmail, ExistingUserName, ExistingPhoneNumber, NotExistingTopicTypes,
    TopicIdsNotFound, CheckUserFound, CheckCourseFound,
)
def _resolve_union_type(obj, info):
    return type(obj)


class CreateCoursesResponse(graphene.Union):
    class Meta:
        types = (CoursesType,DuplicateTitlesInRequest,TitleAlreadyExistsInDB,InvalidLevelType,)
    resolve_type = staticmethod(_resolve_union_type)

class GetCoursesResponse(graphene.Union):
    class Meta:
        types = (CoursesType,DuplicateCourseIdsInRequest,CourseIdsNotFound,)
    resolve_type = staticmethod(_resolve_union_type)

class UpdateCoursesResponse(graphene.Union):
    class Meta:
        types = (CoursesType,DuplicateTitlesInRequest,TitleAlreadyExistsInDB,InvalidLevelType,DuplicateCourseIdsInRequest,CourseIdsNotFound)
    resolve_type = staticmethod(_resolve_union_type)


class CreateTopicsResponse(graphene.Union):
    class Meta:
        types = (TopicsType,NotExistingTopicTypes)
    resolve_type = staticmethod(_resolve_union_type)


class GetTopicsResponse(graphene.Union):
    class Meta:
        types = (TopicsType, TopicIdsNotFound, NotExistingTopicTypes)
    resolve_type = staticmethod(_resolve_union_type)



class CreateUserResponse(graphene.Union):
    class Meta:
        types = (UserType,ExistingEmail,ExistingUserName,ExistingPhoneNumber)
    resolve_type = staticmethod(_resolve_union_type)


class CreateFeedbackResponse(graphene.Union):
    class Meta:
        types = (CourseFeedbackType, CheckCourseFound, CheckUserFound)