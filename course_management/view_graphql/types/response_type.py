import graphene

from .types import TopicsType, CourseFeedbackType, VideoType
from .error_types import (
    DuplicateTitlesInRequest,
    TitleAlreadyExistsInDB,
    InvalidLevelType,
    DuplicateCourseIdsInRequest,
    CourseIdsNotFound, ExistingEmail, ExistingUserName, ExistingPhoneNumber, NotExistingTopicTypes,
    TopicIdsNotFound, CheckUserFound, CheckCourseFound, TopicIdNotFoundType,
)

from course_management.view_graphql.types.types import CourseType, ModuleType, \
    TopicGQLType, EnrollmentType, LearningPathType, UserLearningPathType, \
    LearningUnitType, UserLearningUnitType, CoursesType, \
    ModuleList, UserType, TopicsListType, UserLearningPathPercentageType, \
    UserCurrentLearningUnitStatusType, UpdateLearningUnitProgressType, \
    GetUserCourseCompletionPercentageType, GetModuleCompletionPercentageType, \
    GetTopicCompletionPercentageType, EnrollmentListType, FeedbackType

from course_management.view_graphql.types.error_types import CourseIdsNotInDB, \
    UserNotFoundType, CourseNotFoundType,  \
    DuplicateCourseTitlesFoundType, DuplicateTitlesFoundType, \
    UnexpectedLevelTypeFoundType, NotExistingTopicTypesFoundType, \
    NotExistingTopicIdsFoundType, NotExistedTopicFoundType, \
    CourseInProgressExceptionType, UserNotEnrolledInModuleType, \
    UserLearningPathNotFoundType, LearningUnitIdNotFoundType, \
    LearningUnitLockedExceptionType, LearningPathNotFoundType, \
    AlreadyExistedTitlesFoundType, ExistedUsernameFoundType, \
    ExistedEmailFoundType, ExistedPhoneNumberFoundType, \
    UserLearningUnitIdNotFoundType, ModuleIdsNotFoundInDBType


def _resolve_union_type(obj, info):
    return type(obj)


class CreateCoursesResponse(graphene.Union):
    class Meta:
        types = (CoursesType,DuplicateTitlesInRequest,TitleAlreadyExistsInDB,InvalidLevelType,)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, CoursesType):
            return CoursesType
        if isinstance(instance, DuplicateTitlesInRequest):
            return DuplicateTitlesInRequest
        if isinstance(instance, TitleAlreadyExistsInDB):
            return TitleAlreadyExistsInDB
        if isinstance(instance, InvalidLevelType):
            return InvalidLevelType
        return CoursesType

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


class CourseResponse(graphene.Union):
    class Meta:
        types = (
            CourseType,
            CourseNotFoundType,
            DuplicateCourseTitlesFoundType,
            UnexpectedLevelTypeFoundType,
        )


class CourseListResponse(graphene.Union):
    class Meta:
        types = (
            CoursesType,
            CourseNotFoundType,
            CourseIdsNotInDB,
        )


class ModuleResponse(graphene.Union):
    class Meta:
        types = (
            ModuleType,
            ModuleIdsNotFoundInDBType,
            DuplicateTitlesFoundType,
        )

class GetModulesResponse(graphene.Union):
    class Meta:
        types = (
            ModuleList,
            CourseIdsNotInDB
        )

class GetUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFoundType
        )

class ModuleListResponse(graphene.Union):
    class Meta:
        types = (
            ModuleList,
            DuplicateTitlesFoundType,
            AlreadyExistedTitlesFoundType,
            ModuleIdsNotFoundInDBType,
            CourseIdsNotInDB
        )



class TopicResponse(graphene.Union):
    class Meta:
        types = (
            TopicsListType,
            NotExistedTopicFoundType,
            DuplicateTitlesFoundType,
            NotExistingTopicTypesFoundType,
        )

class UpdateTopicResponse(graphene.Union):
    class Meta:
        types = (
            TopicsListType,
            NotExistedTopicFoundType,
            NotExistingTopicTypesFoundType,
        )

    class UpdateTopicResponse(graphene.Union):
        class Meta:
            types = (
                TopicsListType,
                NotExistedTopicFoundType,
                NotExistingTopicTypesFoundType,
            )





class UserResponse(graphene.Union):
    class Meta:
        types = (
            UserNotFoundType,
            UserType,
            ExistedUsernameFoundType,
            ExistedEmailFoundType,
            ExistedPhoneNumberFoundType
        )

class TopicListResponse(graphene.Union):
    class Meta:
        types = (
            TopicsListType,
            NotExistingTopicIdsFoundType,
        )


class EnrollmentResponse(graphene.Union):
    class Meta:
        types = (
            EnrollmentType,
            CourseNotFoundType,
            UserNotFoundType,
            CourseInProgressExceptionType,
        )


class LearningPathResponse(graphene.Union):
    class Meta:
        types = (
            LearningPathType,
            LearningPathNotFoundType,
        )


class UserLearningPathResponse(graphene.Union):
    class Meta:
        types = (
            UserLearningPathType,
            UserNotFoundType,
            CourseNotFoundType,
        )


class LearningUnitResponse(graphene.Union):
    class Meta:
        types = (
            LearningUnitType,
            LearningUnitIdNotFoundType,
            LearningUnitLockedExceptionType,
        )


class UserLearningUnitResponse(graphene.Union):
    class Meta:
        types = (
            UserLearningUnitType,
            UserLearningPathNotFoundType,
            UserNotEnrolledInModuleType,
        )


class CreateCourseResponse(graphene.Union):
    class Meta:
        types = (
            CoursesType,
            DuplicateCourseTitlesFoundType,
            UnexpectedLevelTypeFoundType,
        )



class UpdateCourseResponse(graphene.Union):
    class Meta:
        types = (
            CourseType,
            CourseNotFoundType,
            UnexpectedLevelTypeFoundType,
        )


class CreateModuleResponse(graphene.Union):
    class Meta:
        types = (
            ModuleType,
            DuplicateTitlesFoundType,
        )


class UpdateModuleResponse(graphene.Union):
    class Meta:
        types = (
            ModuleType,
            ModuleIdsNotFoundInDBType,
        )


class CreateTopicResponse(graphene.Union):
    class Meta:
        types = (
            TopicGQLType,
            DuplicateTitlesFoundType,
            NotExistingTopicTypesFoundType,
        )


class CreateEnrollmentResponse(graphene.Union):
    class Meta:
        types = (
            EnrollmentType,
            CourseNotFoundType,
            UserNotFoundType,
            CourseInProgressExceptionType,
        )


class UpdateLearningUnitProgressResponse(graphene.Union):
    class Meta:
        types = (
            UpdateLearningUnitProgressType,
            UserLearningUnitIdNotFoundType,
            LearningUnitLockedExceptionType
        )

class UserLearningPathPercentageResponse(graphene.Union):
    class Meta:
        types = (
            UserLearningPathPercentageType,
            LearningUnitIdNotFoundType,
            UserLearningPathNotFoundType,
        )

class UserCurrentLearningUnitStatusResponse(graphene.Union):
    class Meta:
        types = (
            UserCurrentLearningUnitStatusType,
            LearningUnitIdNotFoundType,
            UserLearningPathNotFoundType,
        )

class GetUserCourseCompletionPercentageResponse(graphene.Union):
    class Meta:
        types = (
            GetUserCourseCompletionPercentageType,
            CourseNotFoundType,
            UserNotFoundType,
        )

class GetModuleCompletionPercentageResponse(graphene.Union):
    class Meta:
        types = (
            GetModuleCompletionPercentageType,
            UserNotFoundType,
            ModuleIdsNotFoundInDBType,
        )


class GetTopicCompletionPercentageResponse(graphene.Union):
    class Meta:
        types = (
            GetTopicCompletionPercentageType,
            UserNotFoundType,
            NotExistedTopicFoundType,
        )

class GetUserEnrollmentsResponse(graphene.Union):
    class Meta:
        types = (
            EnrollmentListType,
            UserNotFoundType,
        )

class GetUserRecommendedCoursesResponse(graphene.Union):
    class Meta:
        types = (
            CoursesType,
            UserNotFoundType,
        )

class GetTopicForCourseResponse(graphene.Union):
    class Meta:
        types = (
            TopicsListType,
            CourseNotFoundType,
        )

class CourseFeedbackResponse(graphene.Union):
    class Meta:
        types = (
            FeedbackType,
            CourseNotFoundType,
            UserNotFoundType,
        )


class GetVideoResponse(graphene.Union):
    class Meta:
        types = (
            VideoType,
            TopicIdNotFoundType,
        )
