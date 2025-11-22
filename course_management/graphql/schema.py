import graphene

from course_management.graphql.mutations import CreateCourse, UpdateCourse, \
    CreateUsers, CreateTopic
from course_management.graphql.queries import GetCourses, GetTopics

QUERY_CLASSES = [GetCourses, GetTopics]

MUTATION_CLASSES = {CreateCourse,UpdateCourse, CreateUsers, CreateTopic}

class Query(*QUERY_CLASSES):
    pass


class Mutation(*MUTATION_CLASSES):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
