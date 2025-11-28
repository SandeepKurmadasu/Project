import graphene

from course_management.view_graphql.resolvers.course_resolvers.get_courses import \
    resolve_get_courses
from course_management.view_graphql.resolvers.topic_resolvers.get_topics import \
    resolve_get_topics
from course_management.view_graphql.resolvers.learning_path_resolvers.get_user_learning_units_resolver import \
    get_user_learning_units_resolver
from course_management.view_graphql.resolvers.video_resolver.get_topic_video_resolver import \
    get_topic_video_resolver
from course_management.view_graphql.types.input_types import GetCoursesParams, \
    GetTopicsParams, GetUserLearningUnitsReqParams, GetTopicVideoReqParams
from course_management.view_graphql.types.response_type import \
    GetCoursesResponse, GetTopicsResponse, GetUserLearningUnitsResponse, \
    GetTopicVideoResponse
from course_management.view_graphql.resolvers.course_resolvers.get_topics_for_course import \
    get_topics_for_course_resolver
from course_management.view_graphql.resolvers.course_resolvers.get_user_recommended_courses_resolver import \
    get_user_recommended_courses_resolver
from course_management.view_graphql.resolvers.enrollment_resolvers.get_user_enrolled_courses import \
    get_user_enrolled_courses_resolver
from course_management.view_graphql.resolvers.module_resolvers.get_module_completion_percentage_resolver import \
    get_module_completion_percentage_resolver
from course_management.view_graphql.resolvers.module_resolvers.get_module_for_course_resolver import \
    get_course_modules_resolver
from course_management.view_graphql.resolvers.course_resolvers.get_user_course_completion_percentage_resolver import \
    get_user_course_completion_percentage
from course_management.view_graphql.resolvers.learning_path_resolvers.get_user_current_learning_unit_status_resolver import \
    get_user_current_learning_unit_status_resolver
from course_management.view_graphql.resolvers.learning_path_resolvers.get_user_learning_path_percentage_resolver import \
    get_user_learning_path_percentage_resolver
from course_management.view_graphql.resolvers.learning_path_resolvers.get_user_learning_path_resolver import \
    get_user_learning_path_resolver
from course_management.view_graphql.resolvers.topic_resolvers.get_topic_completion_percentage_resolver import \
    get_user_topic_completion_percentage
from course_management.view_graphql.resolvers.user_resolvers.get_user_resolver import \
    get_user_profile_resolver
from course_management.view_graphql.types.input_types import \
    GetModulesForCourse, GetUserReqParms, GetUserLearningPathReqParams, \
    GetUserCourseCompletionReqParams, GetUserModulePercentageReqParams, \
    GetUserTopicCompletionPercentageReqParams, GetUserEnrolledCourses, \
    GetRecommendedCoursesReqParams, GetTopicsForCourseReqParams
from course_management.view_graphql.types.response_type import \
    GetModulesResponse, GetUserResponse, UserLearningPathResponse, \
    UserLearningPathPercentageResponse, UserCurrentLearningUnitStatusResponse, \
    GetUserCourseCompletionPercentageResponse, \
    GetModuleCompletionPercentageResponse, \
    GetTopicCompletionPercentageResponse, GetUserEnrollmentsResponse, \
    GetUserRecommendedCoursesResponse, GetTopicForCourseResponse


class GetCourses(graphene.ObjectType):
    get_courses = graphene.Field(
        GetCoursesResponse,
        params=GetCoursesParams(required=True),
        required=True,
        resolver=resolve_get_courses,
    )


class GetTopics(graphene.ObjectType):
    get_topics = graphene.Field(
        GetTopicsResponse,
        params=GetTopicsParams(required=True),
        required=True,
        resolver=resolve_get_topics,
    )


class GetModulesForCourses(graphene.ObjectType):
    get_modules = graphene.Field(
        GetModulesResponse,
        required=True,
        params=GetModulesForCourse(required=True),
        resolver=get_course_modules_resolver
    )


class GetUserProfile(graphene.ObjectType):
    get_user = graphene.Field(
        GetUserResponse,
        required=True,
        params=GetUserReqParms(required=True),
        resolver=get_user_profile_resolver
    )


class GetUserLearningPath(graphene.ObjectType):
    get_user_learning_path = graphene.Field(
        UserLearningPathResponse,
        required=True,
        params=GetUserLearningPathReqParams(required=True),
        resolver=get_user_learning_path_resolver
    )


class GetUserLearningPathPercentage(graphene.ObjectType):
    get_user_learning_path_percentage = graphene.Field(
        UserLearningPathPercentageResponse,
        required=True,
        params=GetUserLearningPathReqParams(required=True),
        resolver=get_user_learning_path_percentage_resolver
    )


class GetUserCurrentLearningUnitSatus(graphene.ObjectType):
    get_user_current_learning_unit_status = graphene.Field(
        UserCurrentLearningUnitStatusResponse,
        required=True,
        params=GetUserLearningPathReqParams(required=True),
        resolver=get_user_current_learning_unit_status_resolver
    )


class GetUserCourseCompletionPercentage(graphene.ObjectType):
    get_user_course_completion_percentage = graphene.Field(
        GetUserCourseCompletionPercentageResponse,
        required=True,
        params=GetUserCourseCompletionReqParams(required=True),
        resolver=get_user_course_completion_percentage
    )


class GetModuleCompletionPercentage(graphene.ObjectType):
    get_module_completion_percentage = graphene.Field(
        GetModuleCompletionPercentageResponse,
        required=True,
        params=GetUserModulePercentageReqParams(required=True),
        resolver=get_module_completion_percentage_resolver
    )


class GetTopicCompletionPercentage(graphene.ObjectType):
    get_topic_completion_percentage = graphene.Field(
        GetTopicCompletionPercentageResponse,
        required=True,
        params=GetUserTopicCompletionPercentageReqParams(required=True),
        resolver=get_user_topic_completion_percentage
    )


class GetUserEnrollments(graphene.ObjectType):
    get_user_enrollments = graphene.Field(
        GetUserEnrollmentsResponse,
        required=True,
        params=GetUserEnrolledCourses(required=True),
        resolver=get_user_enrolled_courses_resolver
    )


class GetUserRecommendedCourses(graphene.ObjectType):
    get_user_recommended_courses = graphene.Field(
        GetUserRecommendedCoursesResponse,
        required=True,
        params=GetRecommendedCoursesReqParams(required=True),
        resolver=get_user_recommended_courses_resolver
    )


class GetTopicsForCourse(graphene.ObjectType):
    get_topics_for_course = graphene.Field(
        GetTopicForCourseResponse,
        required=True,
        params=GetTopicsForCourseReqParams(required=True),
        resolver=get_topics_for_course_resolver
    )


class GetUserLearningUnits(graphene.ObjectType):
    get_user_learning_units = graphene.Field(
        GetUserLearningUnitsResponse,
        required=True,
        params=GetUserLearningUnitsReqParams(required=True),
        resolver=get_user_learning_units_resolver

    )


class GetTopicVideo(graphene.ObjectType):
    get_topic_video = graphene.Field(
        GetTopicVideoResponse,
        required=True,
        params=GetTopicVideoReqParams(required=True),
        resolver=get_topic_video_resolver
    )