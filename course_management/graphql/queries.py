import graphene

from course_management.graphql.resolver.course_resolvers.get_courses import resolve_get_courses
from course_management.graphql.resolver.course_resolvers.get_topics import resolve_get_topics
from course_management.graphql.types.input_types import GetCoursesParams, GetTopicsParams
from course_management.graphql.types.response_types import GetCoursesResponse, GetTopicsResponse


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
        params = GetTopicsParams(required=True),
        required=True,
        resolver=resolve_get_topics,
    )
